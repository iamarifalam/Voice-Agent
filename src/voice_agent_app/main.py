from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import jinja2

from voice_agent_app.knowledge import KnowledgeBase, load_knowledge
from voice_agent_app.models import (
    AgentResponse,
    CallStartRequest,
    CallStartResponse,
    DashboardResponse,
    HealthResponse,
    SessionSummary,
    TranscriptRequest,
)
from voice_agent_app.monitoring import RequestTimer, metrics
from voice_agent_app.orchestrator import SessionStore, build_response
from voice_agent_app.telephony import gather_twiml, say_twiml

ROOT = Path(__file__).resolve().parents[2]
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(ROOT / "templates")),
    autoescape=True
)
env.cache = None  # Disable caching
app = FastAPI(title="CallPilot Voice Ops")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

knowledge_base = KnowledgeBase(load_knowledge(ROOT))
session_store = SessionStore()


@app.get("/", response_class=HTMLResponse)
def voice_home(request: Request) -> HTMLResponse:
    template = env.get_template("index.html")
    context = {
        "request": request,
        "articles": knowledge_base.articles,
        "starter_prompts": [
            "Where is my order right now?",
            "I need to reschedule my appointment to tomorrow afternoon.",
            "What is your return policy for damaged products?",
            "I'm upset and want to speak to a manager now.",
        ],
        "app_name": "CallPilot Voice Ops",
    }
    html_content = template.render(**context)
    return HTMLResponse(content=html_content)


@app.post("/api/session", response_model=CallStartResponse)
def start_session(payload: CallStartRequest) -> CallStartResponse:
    with RequestTimer():
        metrics.increment("voice_session_start")
        session = session_store.create(payload.caller_name, payload.phone_number)
        greeting = (
            f"Hello {payload.caller_name}, you are connected to CallPilot Voice Ops. "
            "How can I help you today?"
        )
        return CallStartResponse(session_id=session.session_id, greeting=greeting)


@app.post("/api/respond", response_model=AgentResponse)
def respond(payload: TranscriptRequest) -> AgentResponse:
    with RequestTimer():
        metrics.increment("voice_turn")
        try:
            session = session_store.get(payload.session_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Unknown session") from exc
        hits = knowledge_base.search(payload.transcript)
        result = build_response(session, payload.transcript, hits)
        if result.escalation_required:
            metrics.increment("voice_escalation")
        return result


@app.post("/webhooks/twilio/voice", response_class=PlainTextResponse)
def inbound_voice() -> str:
    metrics.increment("voice_webhook")
    return gather_twiml(
        "Welcome to CallPilot Voice Ops. Please tell me what you need help with.",
        "/webhooks/twilio/process",
    )


@app.post("/webhooks/twilio/process", response_class=PlainTextResponse)
def process_voice(speech_result: str = Form(default="")) -> str:
    metrics.increment("voice_webhook_process")
    if not speech_result:
        return say_twiml("I did not catch that. Please call again when ready.")
    hits = knowledge_base.search(speech_result)
    shadow_session = session_store.create("Twilio Caller", "unknown")
    result = build_response(shadow_session, speech_result, hits)
    return say_twiml(result.response_text)


@app.get("/api/dashboard", response_model=DashboardResponse)
def dashboard() -> DashboardResponse:
    voice_turns = metrics.counters.get("voice_turn", 0)
    voice_escalations = metrics.counters.get("voice_escalation", 0)
    recent_sessions = [
        SessionSummary(
            session_id=session.session_id,
            caller_name=session.caller_name,
            phone_number=session.phone_number,
            turn_count=len(session.turns),
            latest_intent=session.latest_intent,
            escalation_required=session.escalation_required,
        )
        for session in session_store.recent()
    ]
    return DashboardResponse(
        active_sessions=len(session_store.sessions),
        total_turns=voice_turns,
        total_escalations=voice_escalations,
        knowledge_articles=len(knowledge_base.articles),
        recent_sessions=recent_sessions,
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        active_sessions=len(session_store.sessions),
        articles=len(knowledge_base.articles),
        generated_at=datetime.now(timezone.utc),
    )


@app.get("/metrics")
def get_metrics() -> PlainTextResponse:
    """Prometheus-compatible metrics endpoint"""
    lines = []
    for key, value in metrics.counters.items():
        lines.append(f"voice_agent_{key}_total {value}")
    if metrics.latency_samples:
        avg_latency = sum(metrics.latency_samples) / len(metrics.latency_samples)
        lines.append(f"voice_agent_request_duration_seconds_avg {avg_latency:.6f}")
    lines.append(f"voice_agent_active_sessions {len(session_store.sessions)}")
    lines.append(f"voice_agent_knowledge_articles {len(knowledge_base.articles)}")
    return PlainTextResponse("\n".join(lines) + "\n")

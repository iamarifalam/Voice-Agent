from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone

from voice_agent_app.models import AgentResponse, ConversationTurn, Intent, Sentiment, SourceItem


ORDER_KEYWORDS = {"order", "shipment", "delivery", "tracking", "package", "dispatch"}
APPOINTMENT_KEYWORDS = {"appointment", "schedule", "book", "reschedule", "calendar", "demo"}
ESCALATION_KEYWORDS = {"agent", "manager", "complaint", "refund", "cancel", "angry", "human"}
FAQ_KEYWORDS = {"return", "pricing", "hours", "support", "policy", "warranty"}
FRUSTRATED_KEYWORDS = {"angry", "upset", "frustrated", "terrible", "bad", "complaint"}


@dataclass(slots=True)
class CallSession:
    session_id: str
    caller_name: str
    phone_number: str
    turns: list[ConversationTurn] = field(default_factory=list)
    latest_intent: Intent | None = None
    escalation_required: bool = False


class SessionStore:
    def __init__(self) -> None:
        self.sessions: dict[str, CallSession] = {}

    def create(self, caller_name: str, phone_number: str) -> CallSession:
        session = CallSession(
            session_id=secrets.token_hex(8),
            caller_name=caller_name,
            phone_number=phone_number,
        )
        self.sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> CallSession:
        return self.sessions[session_id]

    def recent(self, limit: int = 6) -> list[CallSession]:
        return sorted(
            self.sessions.values(),
            key=lambda session: session.turns[-1].created_at if session.turns else datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )[:limit]


def infer_intent(text: str) -> Intent:
    lowered = text.lower()
    tokens = set(lowered.split())
    if tokens & ESCALATION_KEYWORDS:
        return "escalate"
    if tokens & ORDER_KEYWORDS:
        return "order_status"
    if tokens & APPOINTMENT_KEYWORDS:
        return "appointment"
    if tokens & FAQ_KEYWORDS:
        return "faq"
    return "unknown"


def infer_sentiment(text: str) -> Sentiment:
    lowered = text.lower()
    return "frustrated" if any(word in lowered for word in FRUSTRATED_KEYWORDS) else "calm"


def build_response(session: CallSession, transcript: str, knowledge_hits: list) -> AgentResponse:
    now = datetime.now(timezone.utc)
    session.turns.append(ConversationTurn(speaker="caller", text=transcript, created_at=now))

    intent = infer_intent(transcript)
    sentiment = infer_sentiment(transcript)
    escalation_required = intent == "escalate" or sentiment == "frustrated"

    if escalation_required:
        response_text = (
            "I’m routing this to a human support specialist now. "
            "I’ve captured your issue summary so you do not need to repeat it."
        )
    elif knowledge_hits:
        summaries = " ".join(article.content.splitlines()[0] for article in knowledge_hits)
        response_text = f"Here’s what I found: {summaries}"
    elif intent == "appointment":
        response_text = (
            "I can help schedule that. Available demo windows are weekdays at 11 AM, 2 PM, and 4 PM."
        )
    elif intent == "order_status":
        response_text = (
            "I can help with order status. Please share your order number and I’ll verify the latest milestone."
        )
    else:
        response_text = (
            "I can help with order status, appointments, returns, warranty questions, or transfer you to a human agent."
        )

    session.latest_intent = intent
    session.escalation_required = escalation_required
    session.turns.append(ConversationTurn(speaker="agent", text=response_text, created_at=now))
    return AgentResponse(
        session_id=session.session_id,
        intent=intent,
        sentiment=sentiment,
        response_text=response_text,
        escalation_required=escalation_required,
        sources=[
            SourceItem(article_id=article.article_id, title=article.title, topic=article.topic)
            for article in knowledge_hits
        ],
        transcript=[{"speaker": turn.speaker, "text": turn.text} for turn in session.turns],
    )

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Intent = Literal["faq", "order_status", "appointment", "escalate", "unknown"]
Sentiment = Literal["calm", "frustrated"]


@dataclass(slots=True)
class KnowledgeArticle:
    article_id: str
    title: str
    topic: str
    content: str
    keywords: frozenset[str] = field(default_factory=frozenset)


@dataclass(slots=True)
class ConversationTurn:
    speaker: Literal["caller", "agent"]
    text: str
    created_at: datetime


class CallStartRequest(BaseModel):
    caller_name: str = Field(min_length=2, max_length=80)
    phone_number: str = Field(min_length=7, max_length=32)


class CallStartResponse(BaseModel):
    session_id: str
    greeting: str


class TranscriptRequest(BaseModel):
    session_id: str
    transcript: str = Field(min_length=2, max_length=1200)


class SourceItem(BaseModel):
    article_id: str
    title: str
    topic: str


class AgentResponse(BaseModel):
    session_id: str
    intent: Intent
    sentiment: Sentiment
    response_text: str
    escalation_required: bool
    sources: list[SourceItem]
    transcript: list[dict[str, str]]


class HealthResponse(BaseModel):
    status: str
    active_sessions: int
    articles: int
    generated_at: datetime


class SessionSummary(BaseModel):
    session_id: str
    caller_name: str
    phone_number: str
    turn_count: int
    latest_intent: Intent | None = None
    escalation_required: bool = False


class DashboardResponse(BaseModel):
    active_sessions: int
    total_turns: int
    total_escalations: int
    knowledge_articles: int
    recent_sessions: list[SessionSummary]

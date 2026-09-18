from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Comment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    author: str
    body: str
    created_at: datetime = Field(default_factory=utc_now)


class Action(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    action: str
    actor: str
    created_at: datetime = Field(default_factory=utc_now)


class Case(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    summary: str
    status: str = "open"
    diagnosis: str | None = None
    comments: list[Comment] = Field(default_factory=list)
    actions: list[Action] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

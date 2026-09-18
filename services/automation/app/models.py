from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class ExecutionRequest(BaseModel):
    action: str
    target_container: str = Field(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,62}$")


class ExecutionAudit(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    action: str
    target_container: str
    status: str
    output: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

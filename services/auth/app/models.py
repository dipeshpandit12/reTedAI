from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


Role = Literal["analyst", "approver", "admin"]


class User(BaseModel):
    id: str
    email: str
    name: str
    role: Role


class DevelopmentTokenRequest(BaseModel):
    email: str = Field(default="demo@retedai.local", pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    name: str = Field(default="Demo Analyst", min_length=2, max_length=120)
    role: Role = "approver"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


class Session(BaseModel):
    token: str
    user: User
    expires_at: datetime

    def expired(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)

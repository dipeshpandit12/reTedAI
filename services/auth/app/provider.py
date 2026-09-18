import os
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from .models import DevelopmentTokenRequest, Session, TokenResponse, User


class SessionStore:
    """In-memory development store; replace with Keycloak token verification."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def issue_development_token(self, payload: DevelopmentTokenRequest) -> TokenResponse:
        if os.getenv("AUTH_MODE", "disabled") != "development":
            raise RuntimeError("Development authentication is disabled")

        ttl = 3600
        token = secrets.token_urlsafe(32)
        user = User(
            id=str(uuid4()),
            email=payload.email,
            name=payload.name,
            role=payload.role,
        )
        self._sessions[token] = Session(
            token=token,
            user=user,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=ttl),
        )
        return TokenResponse(access_token=token, expires_in=ttl, user=user)

    def resolve(self, token: str) -> User | None:
        session = self._sessions.get(token)
        if session is None or session.expired():
            self._sessions.pop(token, None)
            return None
        return session.user

    def revoke(self, token: str) -> None:
        self._sessions.pop(token, None)


sessions = SessionStore()

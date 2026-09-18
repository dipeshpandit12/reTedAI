from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .models import DevelopmentTokenRequest, TokenResponse, User
from .provider import sessions

app = FastAPI(title="reTedAI Auth Service", version="0.1.0")
bearer = HTTPBearer(auto_error=False)


def credentials(
    value: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> HTTPAuthorizationCredentials:
    if value is None:
        raise HTTPException(status_code=401, detail="Bearer token required")
    return value


@app.get("/health")
@app.get("/auth/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "auth"}


@app.post("/auth/dev-token", response_model=TokenResponse)
def create_development_token(payload: DevelopmentTokenRequest) -> TokenResponse:
    try:
        return sessions.issue_development_token(payload)
    except RuntimeError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.get("/auth/me", response_model=User)
def current_user(value: HTTPAuthorizationCredentials = Depends(credentials)) -> User:
    user = sessions.resolve(value.credentials)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


@app.delete("/auth/session", status_code=status.HTTP_204_NO_CONTENT)
def revoke_session(value: HTTPAuthorizationCredentials = Depends(credentials)) -> Response:
    sessions.revoke(value.credentials)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import Depends, FastAPI, HTTPException, status

from .db import repository
from .deps import CurrentUser, get_current_user
from .events import emit_case_created
from .models import Case
from .schemas import ApproveCaseRequest, CreateCaseRequest

app = FastAPI(title="reTedAI Case Service", version="0.2.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "case"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "case"}


@app.get("/cases", response_model=list[Case])
def list_cases() -> list[Case]:
    return repository.list()


@app.post("/cases", response_model=Case, status_code=status.HTTP_201_CREATED)
def create_case(
    payload: CreateCaseRequest,
    user: CurrentUser = Depends(get_current_user),
) -> Case:
    item = repository.create(payload, user)
    emit_case_created(item)
    return item


@app.get("/cases/{case_id}", response_model=Case)
def get_case(case_id: str) -> Case:
    item = repository.get(case_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return item


@app.post("/cases/{case_id}/approve", response_model=Case)
def approve_case(
    case_id: str,
    payload: ApproveCaseRequest,
    user: CurrentUser = Depends(get_current_user),
) -> Case:
    if user.role not in {"approver", "admin"}:
        raise HTTPException(status_code=403, detail="Approver role required")
    item = repository.approve(case_id, payload, user)
    if item is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return item

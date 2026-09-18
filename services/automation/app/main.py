from fastapi import FastAPI

from .models import ExecutionAudit, ExecutionRequest
from .runner import run
from .whitelist import ACTIONS

app = FastAPI(title="reTedAI Automation Service", version="0.1.0")
audit_log: list[ExecutionAudit] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "automation"}


@app.get("/actions")
def list_actions() -> list[dict[str, str]]:
    return [{"name": action.name, "description": action.description} for action in ACTIONS.values()]


@app.post("/executions", response_model=ExecutionAudit)
def execute(payload: ExecutionRequest) -> ExecutionAudit:
    audit = run(payload)
    audit_log.append(audit)
    return audit


@app.get("/executions", response_model=list[ExecutionAudit])
def list_executions() -> list[ExecutionAudit]:
    return audit_log

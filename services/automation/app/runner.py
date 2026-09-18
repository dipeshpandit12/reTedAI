import os
import subprocess

from .models import ExecutionAudit, ExecutionRequest
from .whitelist import ACTIONS


def run(request: ExecutionRequest) -> ExecutionAudit:
    action = ACTIONS.get(request.action)
    if action is None:
        return ExecutionAudit(action=request.action, target_container=request.target_container, status="rejected", output="Action is not whitelisted.")

    if os.getenv("ENABLE_AUTOMATION_EXECUTION", "false").lower() != "true":
        return ExecutionAudit(action=request.action, target_container=request.target_container, status="dry-run", output=f"Would run: docker exec {request.target_container} {' '.join(action.command)}")

    completed = subprocess.run(
        ["docker", "exec", request.target_container, *action.command],
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    return ExecutionAudit(
        action=request.action,
        target_container=request.target_container,
        status="succeeded" if completed.returncode == 0 else "failed",
        output=(completed.stdout or completed.stderr)[-8000:],
    )

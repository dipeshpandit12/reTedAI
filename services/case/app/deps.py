from typing import Literal

from fastapi import Header
from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: str
    role: Literal["analyst", "approver", "admin"]


def get_current_user(
    user_id: str = Header(default="local-user", alias="x-user-id"),
    role: Literal["analyst", "approver", "admin"] = Header(
        default="analyst", alias="x-user-role"
    ),
) -> CurrentUser:
    # Keycloak seam: validate a bearer token and map its claims here.
    return CurrentUser(id=user_id, role=role)

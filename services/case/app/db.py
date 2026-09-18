from threading import Lock

from .deps import CurrentUser
from .models import Action, Case, utc_now
from .schemas import ApproveCaseRequest, CreateCaseRequest


class CaseRepository:
    """In-memory development repository; replace with PostgreSQL persistence."""

    def __init__(self) -> None:
        self._items: dict[str, Case] = {}
        self._lock = Lock()

    def list(self) -> list[Case]:
        return sorted(self._items.values(), key=lambda item: item.created_at, reverse=True)

    def get(self, case_id: str) -> Case | None:
        return self._items.get(case_id)

    def create(self, payload: CreateCaseRequest, user: CurrentUser) -> Case:
        item = Case(title=payload.title, summary=payload.summary)
        item.actions.append(Action(action="case.created", actor=user.id))
        with self._lock:
            self._items[item.id] = item
        return item

    def approve(
        self,
        case_id: str,
        payload: ApproveCaseRequest,
        user: CurrentUser,
    ) -> Case | None:
        with self._lock:
            item = self._items.get(case_id)
            if item is None:
                return None
            item.status = "approved"
            item.updated_at = utc_now()
            item.actions.append(
                Action(action=f"diagnosis.approved: {payload.note}", actor=user.id)
            )
            return item


repository = CaseRepository()

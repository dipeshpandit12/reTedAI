import json
import logging

from .models import Case

logger = logging.getLogger(__name__)


def emit_case_created(item: Case) -> None:
    """RabbitMQ seam; currently logs an event envelope for local execution."""
    event = {"type": "case.created", "case_id": item.id, "title": item.title}
    logger.info("event=%s", json.dumps(event))

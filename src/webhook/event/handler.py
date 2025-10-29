import time
import uuid
from fastapi import HTTPException

from .models import BaseEventPayload
from .wrapper import event_handlers
from ..utils.logger import get_logger

logger = get_logger(__name__)

async def event_handler(payload: BaseEventPayload):
    """Generic event handler that routes to specific handlers based on event name."""
    request_id = payload.id
    start_time = time.time()
    event_name = payload.trigger.name

    logger.info(f"[{event_name}] Start processing | request_id={request_id}")

    try:
        # Check if event exists
        if event_name not in event_handlers:
            error_msg = f"Unknown event: {event_name}"
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"[{event_name}] Unknown event | request_id={request_id} | duration_ms={duration_ms:.2f} | error={error_msg}"
            )
            raise HTTPException(status_code=400, detail=error_msg)

        handler = event_handlers[event_name]

        logger.debug(f"[{event_name}] Input validated | request_id={request_id}")

        # Execute event
        result = await handler(payload.event)

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"[{event_name}] Success | request_id={request_id} | duration_ms={duration_ms:.2f}"
        )

        return result

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.exception(
            f"[{event_name}] Failed | request_id={request_id} | duration_ms={duration_ms:.2f} | error={str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))

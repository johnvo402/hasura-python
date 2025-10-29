import time
import uuid
from fastapi import HTTPException

from .models import BaseActionPayload
from .wrapper import action_handlers
from ..utils.logger import get_logger

logger = get_logger(__name__)

async def action_handler(payload: BaseActionPayload):
    """Generic action handler that routes to specific handlers based on action name."""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    action_name = payload.action.name

    logger.info(f"[{action_name}] Start processing | request_id={request_id}")

    try:
        # Check if action exists
        if action_name not in action_handlers:
            error_msg = f"Unknown action: {action_name}"
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"[{action_name}] Unknown action | request_id={request_id} | duration_ms={duration_ms:.2f} | error={error_msg}"
            )
            raise HTTPException(status_code=400, detail=error_msg)

        # Get handler & model
        handler = action_handlers[action_name]

        logger.debug(f"[{action_name}] Input validated | request_id={request_id}")

        # Execute action
        result = await handler(payload)

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"[{action_name}] Success | request_id={request_id} | duration_ms={duration_ms:.2f}"
        )

        return result

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.exception(
            f"[{action_name}] Failed | request_id={request_id} | duration_ms={duration_ms:.2f} | error={str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))

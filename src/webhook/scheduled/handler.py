import time
import uuid
from fastapi import HTTPException

from .models import ScheduleModel
from .wrapper import schedule_handlers
from ..utils.logger import get_logger

logger = get_logger(__name__)

async def schedule_handler(payload: ScheduleModel):
    """Generic schedule handler that routes to specific handlers based on schedule name."""
    request_id = payload.id
    start_time = time.time()
    schedule_name = payload.name
    schedule_time = payload.scheduled_time.timetz()


    logger.info(f"[{schedule_name}] Start processing | request_id={request_id} | schedule time={schedule_time}")

    try:
        # Check if schedule exists
        if schedule_name not in schedule_handlers:
            error_msg = f"Unknown schedule: {schedule_name}"
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"[{schedule_name}] Unknown schedule | request_id={request_id} | duration_ms={duration_ms:.2f} | error={error_msg}"
            )
            raise HTTPException(status_code=400, detail=error_msg)

        handler = schedule_handlers[schedule_name]

        logger.debug(f"[{schedule_name}] Input validated | request_id={request_id}")

        # Execute schedule
        result = await handler(payload)

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"[{schedule_name}] Success | request_id={request_id} | duration_ms={duration_ms:.2f}"
        )

        return result

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.exception(
            f"[{schedule_name}] Failed | request_id={request_id} | duration_ms={duration_ms:.2f} | error={str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))

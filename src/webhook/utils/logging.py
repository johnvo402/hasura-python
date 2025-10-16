import logging
import json
from datetime import datetime
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("action_logger")

def format_log_message(
    action_name: str,
    request_id: str,
    headers: Dict[str, str],
    input_data: Any,
    duration_ms: float,
    status_code: int,
    response: Any = None,
    error: str = None
) -> str:
    """Format a structured log message for actions"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "action": action_name,
        "duration_ms": duration_ms,
        "status_code": status_code,
        "headers": headers,
        "input": input_data,
    }
    
    if response is not None:
        log_data["response"] = response
    if error is not None:
        log_data["error"] = error
        
    return json.dumps(log_data, indent=2)

def log_action_request(
    action_name: str,
    request_id: str,
    headers: Dict[str, str],
    input_data: Any
) -> None:
    """Log action request details"""
    logger.info(f"Action Request - {action_name}\n" + format_log_message(
        action_name=action_name,
        request_id=request_id,
        headers=headers,
        input_data=input_data,
        duration_ms=0,
        status_code=0
    ))

def log_action_response(
    action_name: str,
    request_id: str,
    headers: Dict[str, str],
    input_data: Any,
    duration_ms: float,
    status_code: int,
    response: Any = None,
    error: str = None
) -> None:
    """Log action response details"""
    if error:
        logger.error(f"Action Error - {action_name}\n" + format_log_message(
            action_name=action_name,
            request_id=request_id,
            headers=headers,
            input_data=input_data,
            duration_ms=duration_ms,
            status_code=status_code,
            error=error
        ))
    else:
        logger.info(f"Action Response - {action_name}\n" + format_log_message(
            action_name=action_name,
            request_id=request_id,
            headers=headers,
            input_data=input_data,
            duration_ms=duration_ms,
            status_code=status_code,
            response=response
        ))
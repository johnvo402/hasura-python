import time
import uuid
from fastapi import HTTPException, Request
from .models import BaseActionPayload
from .wrapper import action_handlers
from ..utils.logging import log_action_request, log_action_response

async def action_handler(request: Request, payload: BaseActionPayload):
    """Generic action handler that routes to specific handlers based on action name"""
    # Generate unique request ID for tracking
    request_id = str(uuid.uuid4())
    start_time = time.time()
    action_name = payload.action.name
    
    # Get headers as dict
    headers = dict(request.headers)
    
    # Log incoming request
    log_action_request(
        action_name=action_name,
        request_id=request_id,
        headers=headers,
        input_data=payload.dict()
    )
    
    try:
        # Check if action exists
        if action_name not in action_handlers:
            error_msg = f"Unknown action: {action_name}"
            duration_ms = (time.time() - start_time) * 1000
            log_action_response(
                action_name=action_name,
                request_id=request_id,
                headers=headers,
                input_data=payload.dict(),
                duration_ms=duration_ms,
                status_code=400,
                error=error_msg
            )
            raise HTTPException(
                status_code=400,
                detail=error_msg
            )
        
        # Get the appropriate handler and model for this action
        input_model, handler = action_handlers[action_name]
        
        # Validate the input data using the appropriate model
        action_data = input_model(**payload.input["data"])
        
        # Call the specific handler
        result = await handler(action_data)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
    
            
        return result
        
    except Exception as e:
        # Calculate duration and log error
        duration_ms = (time.time() - start_time) * 1000
        log_action_response(
            action_name=action_name,
            request_id=request_id,
            headers=headers,
            input_data=payload.dict(),
            duration_ms=duration_ms,
            status_code=400,
            error=str(e)
        )
        
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
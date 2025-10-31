from fastapi import APIRouter, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import os
from datetime import datetime, timedelta
import jwt

from .actions import action_handler, BaseActionPayload
from .event import event_handler, BaseEventPayload
from .auth import verify_token_handler
from .scheduled import ScheduleModel, schedule_handler

router = APIRouter()


# ---------- Hasura webhook routes ----------
@router.post("/verify-token")
async def verify_token(request: Request):
    return await verify_token_handler(request)


# ---------- Action routes ----------
@router.post("/action")
async def handle_action(request: Request, payload: BaseActionPayload):
    response = await action_handler(payload)
    if not response.success:
        return JSONResponse(content=response.error, status_code=response.status_code)
    return response.data


# ---------- Event trigger handler ----------
@router.post("/event")
async def handle_event(request: Request, payload: BaseEventPayload):
    response = await event_handler(payload)
    if not response.success:
        return JSONResponse(content=response.error, status_code=response.status_code)
    return response.data


# ---------- Scheduled event handler ----------
@router.post("/scheduled")
async def scheduled_run(payload: ScheduleModel):
    response = await schedule_handler(payload)
    if not response.success:
        return JSONResponse(content=response.error, status_code=response.status_code)
    return response.data


@router.get("/health")
def health_check():
    return JSONResponse(
        content={"status": "ok", "message": "FastAPI is running"}, status_code=200
    )

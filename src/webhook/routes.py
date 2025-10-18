from fastapi import APIRouter, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import os
from datetime import datetime, timedelta
import jwt

from .actions import action_handler, BaseActionPayload
from .auth import verify_token_handler

router = APIRouter()

# ---------- Hasura webhook routes ----------
@router.post("/verify-token")
async def verify_token(request: Request):
    return await verify_token_handler(request)

# ---------- Action routes ----------
@router.post("/action")
async def handle_action(request: Request, payload: BaseActionPayload):
    response = await action_handler(request, payload)
    if not response.success:
        return JSONResponse(content=response.error, status_code=response.status_code)
    return response.data

# ---------- Event trigger handler ----------
@router.post("/events/order_insert")
async def order_insert_handler(request: Request, x_hasura_event_id: str | None = Header(None)):
    body = await request.json()
    # Optionally verify HMAC header / secret:
    # verify_signature(request_body_bytes, request.headers.get("x-hasura-signature"), WEBHOOK_SECRET)
    # body has shape: { "event": { "session_variables": {...}, "op": "INSERT", "data": { "old": null, "new": {...}}}, "trace_context": {...}, "delivery_info": {...} }
    event = body.get("event", {})
    op = event.get("op")
    new_row = event.get("data", {}).get("new")
    # enqueue background job or process immediately
    # e.g., await task_queue.enqueue("handle_order", new_row)
    return {"status": "ok"}

# ---------- Scheduled event handler ----------
@router.post("/scheduled/run_daily")
async def scheduled_run_daily(request: Request):
    body = await request.json()
    # Hasura scheduled events deliver payload you set when creating the schedule
    # process job (report generation, cleanup, etc.)
    return {"status": "scheduled_ok"}

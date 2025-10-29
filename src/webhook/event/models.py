from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from ..pkgs import SessionVariable


# Base action models
class EventData(BaseModel):
    old: Optional[Dict[str, Any]] = None
    new: Optional[Dict[str, Any]] = None


class EventContent(BaseModel):
    session_variables: SessionVariable
    op: str
    data: EventData


class TableInfo(BaseModel):
    schema: str
    name: str


class TriggerInfo(BaseModel):
    name: str


class BaseEventPayload(BaseModel):
    id: str
    created_at: datetime
    delivery_info: Dict[str, Any]
    trigger: TriggerInfo
    table: TableInfo
    event: EventContent
    
class EventExtensionResponse(BaseModel):
    location: Optional[str] = None
    path: Optional[str] = None
    
class EventWebhookErrorResponse(BaseModel):
    message: str
    extensions: Optional[EventExtensionResponse] = None
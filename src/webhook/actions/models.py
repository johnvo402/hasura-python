from pydantic import BaseModel
from typing import Optional
from ..pkgs import SessionVariable

# Base action models
class ActionMetadata(BaseModel):
    name: str

class BaseActionPayload(BaseModel):
    action: ActionMetadata
    input: dict
    session_variables: SessionVariable
    
class ActionExtensionResponse(BaseModel):
    location: Optional[str] = None
    path: Optional[str] = None
    
class ActionWebhookErrorResponse(BaseModel):
    message: str
    extensions: Optional[ActionExtensionResponse] = None
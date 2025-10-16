from pydantic import BaseModel

# Base action models
class ActionMetadata(BaseModel):
    name: str

class BaseActionPayload(BaseModel):
    action: ActionMetadata
    input: dict
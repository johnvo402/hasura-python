from pydantic import BaseModel, Field
from typing import Optional, List

class SessionVariable(BaseModel):
    user_id: Optional[str] = Field(default=None, alias="x-hasura-user-id")
    role: Optional[str] = Field(default=None, alias="x-hasura-role")
    permissions: Optional[List[str]] = Field(default=None, alias="x-hasura-permissions")

from pydantic import BaseModel

class LoginData(BaseModel):
    username: str
    password: str

class LoginActionResponse(BaseModel):
    accessToken: str
    refeshToken: str
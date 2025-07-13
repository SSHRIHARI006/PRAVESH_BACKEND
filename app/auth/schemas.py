from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    bt_id: str | None = None

class LoginRequest(BaseModel):
    bt_id: str
    password: str

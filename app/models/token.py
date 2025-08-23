from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    exp: str
    admin: bool = False

class TokenData(BaseModel):
    user_id: Optional[str] = None


class LoginCredentials(BaseModel):
    email: str
    password: str
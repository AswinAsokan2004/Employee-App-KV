from pydantic import BaseModel, EmailStr


class TokenPayload(BaseModel):
    email: EmailStr
    password: str
    exp: int


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RegisterRequest(BaseModel):
      # email, password, role (default 'patient')
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = "patient"

class TokenResponse(BaseModel):
      # access_token, token_type
    access_token: str
    token_type: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
      # id, email, role — no password_hash!
    id: int
    email: EmailStr
    role: str

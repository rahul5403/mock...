from ninja import Schema
from pydantic import EmailStr

class UserCreate(Schema):
    email: EmailStr
    username: str
    password: str

class TokenResponse(Schema):
    access: str

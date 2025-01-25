from pydantic import BaseModel


class UserLoginInSchema(BaseModel):
    username: str
    password: str


class UserRegisterInSchema(UserLoginInSchema):
    confirm_password: str


class TokenOutSchema(BaseModel):
    access_token: str
    refresh_token: str

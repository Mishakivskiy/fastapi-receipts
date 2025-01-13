from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    name: str
    password: str


class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserAuth(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCurrent(BaseModel):
    username: str
    id: int

    class Config:
        orm_mode = True

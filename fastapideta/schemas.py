from datetime import date
from typing import Union
from pydantic import BaseModel


class C(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Item(BaseModel):
    title: str
    text: str
    date_created: date
    category_id: Union[int, None] = None

    class Config:
        orm_mode = True


class ItemResponse(BaseModel):
    id: int
    title: str
    text: str
    date_created: date
    category: Union[C, None] = None

    class Config:
        orm_mode = True


class ItemUpdate(Item):
    title: str
    text: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

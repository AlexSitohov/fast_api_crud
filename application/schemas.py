from datetime import date

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
    category_back_populates: C | None = None

    class Config:
        orm_mode = True


class ItemResponse(Item):
    id: int
    title: str
    text: str
    date_created: date
    category: int | None = None

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

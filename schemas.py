from datetime import date

from pydantic import BaseModel


class Item(BaseModel):
    title: str
    text: str
    date_created: date
    category: int | None = None

    class Config:
        orm_mode = True


class ItemResponse(Item):
    id: int
    title: str
    text: str
    date_created: date

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

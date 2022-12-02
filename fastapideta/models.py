from .database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    date_created = Column(Date)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))

    category = relationship("Category", back_populates="items")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)

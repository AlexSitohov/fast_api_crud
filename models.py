from database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    items = relationship("Item", back_populates="category_back_populates")


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    date_created = Column(Date)
    category = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))

    category_back_populates = relationship("Category", back_populates="items")

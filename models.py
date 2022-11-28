from database import Base
from sqlalchemy import *


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    date_created = Column(Date)

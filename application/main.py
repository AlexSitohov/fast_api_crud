from fastapi import FastAPI
from .database import engine
from . import models
from .routers import items, categories

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(items.router)
app.include_router(categories.router)

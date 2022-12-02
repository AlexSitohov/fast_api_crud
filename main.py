from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapideta.database import engine
from fastapideta import models
from fastapideta.routers import items, categories, users, authentication

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(items.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(authentication.router)

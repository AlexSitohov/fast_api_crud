from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapideta.database import engine
from fastapideta import models
from fastapideta.routers import items, categories, users, authentication, profile

app = FastAPI(description="""## Hello there! Its me))) Sanya The Developer""")

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
app.include_router(profile.router)

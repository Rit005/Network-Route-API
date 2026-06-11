from fastapi import FastAPI

from app.database import engine
from app.database import Base

from app.routes import router

import app.models

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Network Route API"
)

app.include_router(router)
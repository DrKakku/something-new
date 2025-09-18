from __future__ import annotations

from fastapi import FastAPI

from app.api.v1 import api_v1_router
from app.core.config import settings
from app.core.database import Base, engine


def create_app() -> FastAPI:
	app = FastAPI(title=settings.title, version=settings.version)
	app.include_router(api_v1_router, prefix="/api/v1")
	return app


app = create_app()


@app.on_event("startup")
def on_startup() -> None:
	Base.metadata.create_all(bind=engine)

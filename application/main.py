from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from application.core.config import get_settings
from application.db.postgres.db import create_database, purge_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    if get_settings().app.is_debug:
        await create_database()
    yield
    if get_settings().app.is_debug:
        await purge_database()


app = FastAPI(
    title=get_settings().app.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/api/docs")

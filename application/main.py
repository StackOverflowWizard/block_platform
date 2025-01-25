from contextlib import asynccontextmanager

from async_fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

from application.api.v1.handlers.auth import router as auth_router
from application.core.config import get_settings
from application.db.postgres.db import create_database, purge_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    if get_settings().app.is_debug:
        await create_database()
    yield
    if get_settings().app.is_debug:
        await purge_database()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@AuthJWT.load_config
def get_config():
    return get_settings().auth


app = FastAPI(
    title=get_settings().app.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/api/docs")


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

from functools import cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    project_name: str = Field(validation_alias="PROJECT_NAME", default="block_platform")
    project_host: str = Field(
        validation_alias="BLOCK_PLATFORM_APP_HOST", default="0.0.0.0"
    )
    project_port: int = Field(validation_alias="BLOCK_PLATFORM_APP_PORT", default=8000)
    is_debug: bool = Field(validation_alias="DEBUG", default=True)


class PostgresSettings(BaseSettings):
    dbname: str = Field(validation_alias="BLOCK_PLATFORM_DB", default="test_db")
    db_user: str = Field(validation_alias="BLOCK_PLATFORM_USER", default="test_admin")
    password: str = Field(validation_alias="BLOCK_PLATFORM_PASSWORD", default="test")
    host: str = Field(validation_alias="BLOCK_PLATFORM_HOST", default="localhost")
    port: int = Field(validation_alias="BLOCK_PLATFORM_PORT", default=5432)

    @property
    def database_dsn(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    @property
    def database_url(self):
        return f"postgresql://{self.db_user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class AuthJWTSettings(BaseSettings):
    authjwt_secret_key: str = Field(
        validation_alias="BLOCK_PLATFORM_SECRET_KEY", default="secret"
    )
    authjwt_algorithm: str = Field(
        validation_alias="BLOCK_PLATFORM_AUTHJWT_ALGORITHM", default="HS256"
    )


class Settings(BaseSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    auth: AuthJWTSettings = Field(default_factory=AuthJWTSettings)


@cache
def get_settings() -> Settings:
    return Settings()

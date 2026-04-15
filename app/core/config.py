from pydantic import PostgresDsn
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8080

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

class LicenceApi(BaseModel):
    prefix: str = "/api"
    licences: str = "/licences"
    version: str = "/v1"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    db: DatabaseConfig
    api: LicenceApi = LicenceApi()
    secret: str


settings = Settings()

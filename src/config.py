from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: str = 8000


class Prefix(BaseModel):
    post: str = '/posts'
    comment: str = '/comments'


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }


class DatabaseTestConfig(BaseModel):
    url: str
    echo: bool = False


class DockerConfig(BaseModel):
    pg_user: str
    pg_password: str
    pg_db: str
    image: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.env.dev', '../.env.dev'),  # value of next parameter overrides value previous one
        case_sensitive=False,
        env_nested_delimiter='__',
    )
    run: RunConfig = RunConfig()
    prefix: Prefix = Prefix()
    db: DatabaseConfig
    db_test: DatabaseTestConfig
    docker: DockerConfig


settings = Settings()

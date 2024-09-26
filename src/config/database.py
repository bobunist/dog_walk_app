from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DatabaseConfig(BaseSettings):
    """Configuration for the database."""

    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="POSTGRES_",
    )

    user: str
    password: str
    host: str
    port: str
    name: str

    @property
    def url(self) -> str:
        """Concatenate .env db-params to url."""
        db_url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        return db_url


database_config = DatabaseConfig()

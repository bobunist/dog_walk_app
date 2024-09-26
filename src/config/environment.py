from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.utils.mode_enum import ModeEnum

load_dotenv()


class EnvironmentConfig(BaseSettings):
    """Configuration for the app environment."""

    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    mode: ModeEnum


environment_config = EnvironmentConfig()

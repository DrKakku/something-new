from __future__ import annotations

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class SqliteSettings(BaseModel):
	database_path: str = "sqlite+sqlite:///./nutrition.db"
	echo: bool = False


class AppSettings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", case_sensitive=False)

	env: str = "dev"
	title: str = "Nutrition Analysis API"
	version: str = "0.1.0"
	sqlite: SqliteSettings = SqliteSettings()


settings = AppSettings()

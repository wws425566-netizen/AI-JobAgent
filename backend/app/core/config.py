from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置。

    阶段一先使用 SQLite，后续部署阶段再升级到 PostgreSQL。
    """

    app_name: str = "JobAgent"
    database_url: str = "sqlite:///./jobagent.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


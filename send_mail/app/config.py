from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_USE_TLS: bool
    MAIL_USE_SSL: bool
    USE_CREDENTIALS: bool
    TEMPLATE_FOLDER: str


settings = Settings()

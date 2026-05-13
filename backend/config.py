from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False

    subway_stop_id: str = "A06S"
    subway_line: str = "A"

    default_latitude: float = 40.8487
    default_longitude: float = -73.9385

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

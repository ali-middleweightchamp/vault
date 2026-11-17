from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    provider_sim_url: str
    provider_sim_secret: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    model_config = {"env_file": ".env"}


settings = Settings()

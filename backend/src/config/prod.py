from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class EnvironmentSettings(BaseSettings):
    ORIGINS: list[str]
    COOKIE_DOMAIN: str
    COOKIE_SAMESITE: str
    SQL_DATABASE_URL: str
    DB: str
    DNS_VERIFICATION: str
    DNS_RESET_PSW: str
    AUTHJWT_SECRET_KEY: str
    CONFIG_CREDENTIALS_USERNAME: str
    CONFIG_CREDENTIALS_PASSWORD: str
    CONFIG_CREDENTIALS_FROM: str
    CONFIG_CREDENTIALS_SECRET: str
    INFOATUVERA_KEY: str
    INFOATUVERA_SECRET_KEY: str
    INFOATUVERA_NOMBRE: str
    INFOATUVERA_REGION: str
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    
    class Config:
        # Takes the first .env file found based in the order of the list
        env_file = [".env", ".env.local", ".env.prod"]
        for env in env_file:
            if os.path.exists(env):
                env_file = env
                break
        env_file_encoding = "utf-8"


@lru_cache()
def get_env_settings():
    return EnvironmentSettings()

enviro = get_env_settings()

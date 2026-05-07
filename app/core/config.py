import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL  :str
    SECRETE_KEY :str
    ALGORITHM :str ='HS256'
    ACCESS_TOKEN_EXPIRATION_SECONDS :int = 30

    class Config:
        env_file = '.env'


settings = Settings()



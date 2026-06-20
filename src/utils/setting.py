# connection of DB link in .env files

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    DB_CONNECTION_URI: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    EXP_TIME: int
    
    
settings = Settings()    
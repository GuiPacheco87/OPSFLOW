from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url:str="sqlite:///./opsflow.db"
    redis_url:str="redis://localhost:6379/0"
    jwt_secret:str="development-only-secret-at-least-32-characters"
    access_token_expire_minutes:int=480
    cors_origins:str="http://localhost:3000"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()

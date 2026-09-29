from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR=Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    app_name:str="FitBuddy"
    gemini_api_key:str=""
    gemini_workout_model:str="gemini-3.8-flash"
    gemini_tip_model:str="gemini-3.5-flash-lite"
    ai_mode:str="auto"
    database_url:str="sqlite:///./data/fitbuddy.db"
    admin_key:str="fitbuddy-admin"
    model_config=SettingsConfigDict(env_file=BASE_DIR/".env",env_file_encoding="utf-8",extra="ignore")
@lru_cache
def get_settings(): return Settings()

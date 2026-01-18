from pydantic import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    app_name: str = "Fin_AgenticRAG"
    debug: bool = True


settings = Settings()
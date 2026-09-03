import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed_origin: list[str]

def get_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL"),
        cors_allowed_origin=[os.getenv("CORS_ALLOWED_ORIGIN")],
    )

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed_origin: List[str]


def get_settings() -> Settings:
    db_url = os.getenv("DATABASE_URL")
    cors_origin_raw = os.getenv("CORS_ALLOWED_ORIGIN")

    if not db_url:
        raise ValueError("Переменная окружения DATABASE_URL не установлена!")

    if cors_origin_raw:
        cors_list = [
            host.strip() for host in cors_origin_raw.split(",") if host.strip()
        ]
    else:
        cors_list = []

    return Settings(
        DATABASE_URL=db_url,
        cors_allowed_origin=cors_list,
    )


settings = get_settings()

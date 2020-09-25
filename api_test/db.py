import os
from pathlib import Path

import dotenv
from sqlalchemy import create_engine


def get_db_host():
    if Path("/.dockerenv").exists():
        return "postgres"
    else:
        return "localhost"


def get_db_engine():
    dotenv.load_dotenv()
    pw = os.getenv("POSTGRES_PASSWORD")
    host = get_db_host()
    engine = create_engine(f"postgresql+psycopg2://postgres:{pw}@{host}:5432/postgres")
    return engine

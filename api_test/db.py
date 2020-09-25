import os
from pathlib import Path

import dotenv
from sqlalchemy import create_engine


def get_db_engine():
    dotenv.load_dotenv()
    pw = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    engine = create_engine(f"postgresql+psycopg2://postgres:{pw}@{host}:5432/postgres")
    return engine

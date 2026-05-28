# database.py — updated for Azure PostgreSQL
# Works locally (reads .env) AND on Azure (reads App Settings)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator
from dotenv import load_dotenv

load_dotenv()  # loads .env locally; on Azure env vars are already set — no-op

DB_HOST     = os.getenv("DB_HOST",     "localhost")
DB_PORT     = os.getenv("DB_PORT",     "5432")
DB_NAME     = os.getenv("DB_NAME",     "hospital_db")
DB_USER     = os.getenv("DB_USER",     "hms_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_SSL      = os.getenv("DB_SSL",      "prefer")  # "require" on Azure

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Build connect_args based on SSL setting
connect_args = {}
if DB_SSL == "require":
    connect_args["sslmode"] = "require"

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True,    # test connection before use — handles Azure idle timeouts
    pool_recycle=3600,     # recycle connections every hour
)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
import logging
import os
from typing import Generator
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Load .env first
load_dotenv()

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "hospital_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_SSL = os.getenv("DB_SSL", "disable")
APP_ENV = os.getenv("APP_ENV", "development")

AZURE_POSTGRES_SCOPE = "https://ossrdbms-aad.database.windows.net/.default"


def _get_azure_token() -> str:
    """
    Fetch a fresh Managed Identity token.
    Only used in Azure production.
    """
    from azure.identity import ManagedIdentityCredential

    credential = ManagedIdentityCredential()
    token = credential.get_token(AZURE_POSTGRES_SCOPE)

    logger.info("Fetched Managed Identity token")
    return token.token


def _make_engine():
    """
    Build SQLAlchemy engine for either:
    - Local development (password auth)
    - Azure production (Managed Identity auth)
    """

    if APP_ENV.lower() == "production":
        DATABASE_URL = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        def creator():
            import psycopg2

            token = _get_azure_token()

            return psycopg2.connect(
                host=DB_HOST,
                port=int(DB_PORT),
                dbname=DB_NAME,
                user=DB_USER,
                password=token,
                sslmode="require",
            )

        engine = create_engine(
            DATABASE_URL,
            creator=creator,
            pool_pre_ping=True,
            pool_recycle=3000,
            echo=False,
        )

        logger.info("Database engine configured: Azure Managed Identity")

    else:
        # Local development

        DATABASE_URL = os.getenv("DATABASE_URL")

        if not DATABASE_URL:
            db_password = quote_plus(os.getenv("DB_PASSWORD", ""))

            DATABASE_URL = (
                f"postgresql+psycopg2://"
                f"{DB_USER}:{db_password}"
                f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            )

        logger.info(f"Database URL: {DATABASE_URL}")

        connect_args = {}

        if DB_SSL == "require":
            connect_args["sslmode"] = "require"

        engine = create_engine(
            DATABASE_URL,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )

        logger.info("Database engine configured: Local PostgreSQL")

    return engine


class Base(DeclarativeBase):
    pass


engine = _make_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

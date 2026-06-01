# # database.py — updated for Azure PostgreSQL
# # Works locally (reads .env) AND on Azure (reads App Settings)

# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
# from typing import Generator
# from dotenv import load_dotenv

# load_dotenv()  # loads .env locally; on Azure env vars are already set — no-op

# # DB_HOST     = os.getenv("DB_HOST",     "localhost")
# # DB_PORT     = os.getenv("DB_PORT",     "5432")
# # DB_NAME     = os.getenv("DB_NAME",     "hospital_db")
# # DB_USER     = os.getenv("DB_USER",     "hms_user")
# # DB_PASSWORD = os.getenv("DB_PASSWORD", "")
# # DB_SSL      = os.getenv("DB_SSL",      "prefer")  # "require" on Azure

# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_SSL = os.getenv("DB_SSL", "require")

# DATABASE_URL = (
#     f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
#     f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )

# # Build connect_args based on SSL setting
# connect_args = {}
# if DB_SSL == "require":
#     connect_args["sslmode"] = "require"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args=connect_args,
#     echo=False,
#     pool_pre_ping=True,    # test connection before use — handles Azure idle timeouts
#     pool_recycle=3600,     # recycle connections every hour
# )


# class Base(DeclarativeBase):
#     pass


# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# def get_db() -> Generator[Session, None, None]:
#     """FastAPI dependency — yields a DB session per request."""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# database.py — supports both password auth (local) and token auth (Azure)

import os
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.pool import QueuePool
from typing import Generator
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "hospital_db")
DB_USER = os.getenv("DB_USER", "hms_user")
DB_SSL  = os.getenv("DB_SSL",  "prefer")
APP_ENV = os.getenv("APP_ENV", "development")

# Token scope for Azure Database for PostgreSQL
AZURE_POSTGRES_SCOPE = "https://ossrdbms-aad.database.windows.net/.default"


def _get_azure_token() -> str:
    """
    Fetch a fresh Entra ID token for the Managed Identity.
    Called per connection so expired tokens are automatically replaced.
    Only works when running on Azure App Service.
    """
    from azure.identity import ManagedIdentityCredential
    credential = ManagedIdentityCredential()
    token = credential.get_token(AZURE_POSTGRES_SCOPE)
    logger.info("Fetched Managed Identity token for PostgreSQL")
    return token.token


def _make_engine():
    """Build the SQLAlchemy engine with the correct auth for the environment."""

    connect_args = {"sslmode": DB_SSL} if DB_SSL == "require" else {}

    if APP_ENV == "production":
        # ── Azure: token-based auth — no password ────────────────────────────
        # DB_USER is the Managed Identity display name (hms-app-ananya)
        # Password is replaced by a fresh token fetched per connection
        DATABASE_URL = (
            f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        connect_args["sslmode"] = "require"  # always required in Azure

        def creator():
            """Custom connection creator that injects a fresh token as password."""
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
            pool_recycle=3000,   # recycle before token expires (~3600s)
            echo=False,
        )
        logger.info("Database engine configured: Managed Identity token auth")

    else:
        # ── Local: standard password auth from .env ──────────────────────────
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DATABASE_URL = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        engine = create_engine(
            DATABASE_URL,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )
        logger.info("Database engine configured: password auth (local dev)")

    return engine


class Base(DeclarativeBase):
    pass


engine       = _make_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

TOKEN_DETAILS = """
=== Key Technical Details ===

1. pool_recycle=3000:
   Tokens expire in ~3600 seconds (60 min).
   Recycling connections at 3000s (50 min) ensures a fresh token is fetched
   before the existing one expires. Prevents mid-session auth failures.

2. creator= parameter:
   Passing a custom 'creator' function to create_engine() bypasses SQLAlchemy's
   normal URL parsing and calls your function for each new connection.
   This is how we inject a fresh token every 50 minutes.

3. DB_USER on Azure = 'hms-app-ananya' (the MI display name):
   Not 'hmsadmin' anymore. The admin user is only needed for setup.
   The app now connects as the Managed Identity role.

4. AZURE_POSTGRES_SCOPE:
   'https://ossrdbms-aad.database.windows.net/.default'
   This scope tells Entra ID to issue a token for Azure Database for PostgreSQL.
   Without this exact scope, the token will be rejected by PostgreSQL.

5. azure-identity package:
   Add to requirements.txt: azure-identity
   ManagedIdentityCredential() auto-detects the MI on App Service.
   Locally it fails — that's why we branch on APP_ENV.
"""

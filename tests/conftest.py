# === conftest.py: The Complete Setup for HMS v2 Tests ===

# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# ── Test Database (SQLite in-memory) ──────────────────────────────────────────
# "sqlite:///:memory:" = SQLite database stored entirely in RAM
# No file created, no external service needed — perfect for CI
# check_same_thread=False: SQLite usually only allows one thread;
#   this option allows multiple threads (needed for FastAPI async context)
# StaticPool: ensures all connections use the SAME in-memory DB
#   (without this, each connection creates a separate empty database)

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")  # default: runs fresh for EACH test
def test_db():
    """Create all tables before a test, drop all after."""
    Base.metadata.create_all(bind=engine)   # create tables
    yield                                    # test runs here
    Base.metadata.drop_all(bind=engine)     # clean up after test


@pytest.fixture(scope="function")
def client(test_db):
    """TestClient with the real app but a test (SQLite) database."""

    def override_get_db():
        """Replace the real get_db() with one that uses the test DB."""
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # DEPENDENCY OVERRIDE: tell FastAPI to use our test DB session
    # instead of the real get_db() that connects to Azure PostgreSQL
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up: restore real get_db after the test
    app.dependency_overrides.clear()


# === FIXTURE SCOPES — how often the fixture runs ===

#   scope="function"  → runs before/after EACH test function  (default)
#   scope="class"     → runs once per test class
#   scope="module"    → runs once per test file
#   scope="session"   → runs once for the entire test session

#   For HMS tests: scope="function" ensures each test starts with
#   a CLEAN database — no leftover data from previous tests.
#   This makes tests independent and order-insensitive.


# === DEPENDENCY OVERRIDE — the key mechanism ===

#   app.dependency_overrides[get_db] = override_get_db

#   This tells FastAPI: whenever Depends(get_db) is encountered,
#   call override_get_db() instead.
#   The real get_db() (which connects to Azure PostgreSQL) is bypassed.
#   The test app uses SQLite in-memory — portable, fast, zero config.

#   app.dependency_overrides is a dict: {original_dep: replacement_dep}
#   Clearing it with .clear() restores all original dependencies.

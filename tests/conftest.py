# tests/conftest.py

import pytest
from app import app, db

@pytest.fixture()
def client():
    # Use SQLite in-memory DB for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Create tables
    with app.app_context():
        db.create_all()

    # Create test client
    test_client = app.test_client()
    yield test_client

    # Cleanup
    with app.app_context():
        db.drop_all()

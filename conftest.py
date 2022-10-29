import pytest
from main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

@pytest.fixture(scope="module", autouse=True)
def client():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    settings.Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[settings.get_db] = override_get_db
        
    client = TestClient(app)
    return client
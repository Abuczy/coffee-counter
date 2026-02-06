import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Tworze testową bazę w pamięci (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Nadpisuje dependency bazy danych
app.dependency_overrides[get_db] = override_get_db

# Tworze tabele
Base.metadata.create_all(bind=engine)

# Klient testowy
client = TestClient(app)


def test_root():
    """Test strony głównej"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_add_coffee():
    """Test dodawania kawy"""
    response = client.post("/coffee", json={
        "coffee_type": "latte",
        "size": "large"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["coffee_type"] == "latte"
    assert data["size"] == "large"
    assert "id" in data


def test_get_coffees():
    """Test pobierania wszystkich kaw"""
    response = client.get("/coffee")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_stats():
    """Test statystyk"""
    response = client.get("/coffee/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_coffees" in data
    assert "today_coffees" in data


def test_delete_coffee():
    """Test usuwania kawy"""
    # Najpierw dodajemy
    add_response = client.post("/coffee", json={"coffee_type": "espresso"})
    coffee_id = add_response.json()["id"]
    
    # Teraz usuwamy
    delete_response = client.delete(f"/coffee/{coffee_id}")
    assert delete_response.status_code == 200


def test_delete_nonexistent_coffee():
    """Test usuwania nieistniejącej kawy"""
    response = client.delete("/coffee/99999")
    assert response.status_code == 404

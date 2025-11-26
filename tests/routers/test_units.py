import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from models import Unit
import schemas

client = TestClient(app)

# Test data
test_unit_data = {
    "name": "Test Unit",
    "description": "This is a test unit.",
    "imageUrl": "https://example.com/image.jpg",
}

def test_create_unit(client, auth_headers, db_session: Session):
    response = client.post("/units/", json=test_unit_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_unit_data["name"]
    assert data["description"] == test_unit_data["description"]
    assert "id" in data
    unit_id = data["id"]
    
    # Verify the unit was actually created in the database
    unit_in_db = db_session.query(Unit).filter(Unit.id == unit_id).first()
    assert unit_in_db is not None
    assert unit_in_db.name == test_unit_data["name"]

def test_read_units(client, auth_headers, db_session: Session):
    # Create a test unit to ensure there's at least one
    db_unit = Unit(**test_unit_data)
    db_session.add(db_unit)
    db_session.commit()
    db_session.refresh(db_unit)

    response = client.get("/units/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_unit(client, auth_headers, db_session: Session):
    # Create a test unit
    db_unit = Unit(**test_unit_data)
    db_session.add(db_unit)
    db_session.commit()
    db_session.refresh(db_unit)
    unit_id = db_unit.id

    response = client.get(f"/units/{unit_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_unit_data["name"]
    assert data["id"] == unit_id

def test_read_unit_not_found(client, auth_headers):
    response = client.get("/units/9999", headers=auth_headers)
    assert response.status_code == 404

def test_update_unit(client, auth_headers, db_session: Session):
    # Create a test unit
    db_unit = Unit(**test_unit_data)
    db_session.add(db_unit)
    db_session.commit()
    db_session.refresh(db_unit)
    unit_id = db_unit.id

    updated_data = {
        "name": "Updated Unit",
        "description": "This is an updated test unit.",
        "imageUrl": "https://example.com/updated_image.jpg",
    }
    response = client.put(f"/units/{unit_id}", json=updated_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]
    
    # Verify the update in the database
    db_session.refresh(db_unit)
    assert db_unit.name == updated_data["name"]

def test_update_unit_not_found(client, auth_headers):
    updated_data = {
        "name": "Updated Unit",
        "description": "This is an updated test unit.",
        "imageUrl": "https://example.com/updated_image.jpg",
    }
    response = client.put("/units/9999", json=updated_data, headers=auth_headers)
    assert response.status_code == 404

def test_delete_unit(client, auth_headers, db_session: Session):
    # Create a test unit
    db_unit = Unit(**test_unit_data)
    db_session.add(db_unit)
    db_session.commit()
    db_session.refresh(db_unit)
    unit_id = db_unit.id

    response = client.delete(f"/units/{unit_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify the unit was deleted from the database
    unit_in_db = db_session.query(Unit).filter(Unit.id == unit_id).first()
    assert unit_in_db is None

def test_delete_unit_not_found(client, auth_headers):
    response = client.delete("/units/9999", headers=auth_headers)
    assert response.status_code == 404

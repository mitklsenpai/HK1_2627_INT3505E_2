"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""
import pytest
from jsonschema import ValidationError, validate


def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_book_not_found(client):
    response = client.get("/books/999999")
    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"


def test_create_book_without_title(client):
    response = client.post("/books", json={"author": "Test"})
    assert response.status_code == 400
    assert response.get_json()["code"] == "VALIDATION_ERROR"
    assert any(error["field"] == "title" for error in response.get_json()["errors"])


def test_delete_then_get_book(client):
    created = client.post("/books", json={
        "title": "Test Book",
        "author": "Test Author"
    })
    assert created.status_code == 201

    book_id = created.get_json()["id"]

    deleted = client.delete(f"/books/{book_id}")
    assert deleted.status_code == 204
    assert deleted.data == b""

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"


def test_response_extra_field_blocked(client, sample_book):
    # OpenAPI intentionally has a year type error for Lab 2.
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "title", "author", "year", "isbn"],
        "properties": {
            "id": {"type": "integer", "minimum": 1},
            "title": {"type": "string"},
            "author": {"type": "string"},
            "year": {"type": ["integer", "null"]},
            "isbn": {"type": ["string", "null"]},
        },
    }
    response = client.get(f"/books/{sample_book}")
    assert response.status_code == 200
    book = response.get_json()
    assert "password_hash" not in book
    validate(instance=book, schema=schema)

    leaked_book = {**book, "password_hash": "simulated-secret"}
    with pytest.raises(ValidationError) as exc:
        validate(instance=leaked_book, schema=schema)
    assert exc.value.validator == "additionalProperties"

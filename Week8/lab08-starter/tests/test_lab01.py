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


def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_book_not_found(client):
    response = client.get("/books/999999")
    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"


def test_create_book_without_title(client):
    response = client.post("/books", json={"author": "Test"})
    assert response.status_code == 400
    assert "title" in response.get_json()["errors"]


def test_delete_then_get_book(client):
    created = client.post("/books", json={
        "title": "Test Book",
        "author": "Test Author"
    })
    assert created.status_code in (200, 201)

    book_id = created.get_json()["id"]

    deleted = client.delete(f"/books/{book_id}")
    assert deleted.status_code in (200, 204)

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404
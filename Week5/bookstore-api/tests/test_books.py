import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest
from flask import Flask

from models import db, Book, Category
from routes.books import books_bp


@pytest.fixture()
def client(tmp_path):
    # App riêng, DB riêng -> không đụng instance/bookstore.db thật.
    # Không import app.py vì nó tạo engine trỏ vào DB thật ngay khi import.
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{tmp_path / 'test.db'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    app.register_blueprint(books_bp)

    with app.app_context():
        db.create_all()
        tech = Category(name="Tech", slug="tech")
        news = Category(name="News", slug="news")
        db.session.add_all([
            tech, news,
            Book(title="Alpha", price_vnd=10, stock=1, category=tech),
            Book(title="Beta", price_vnd=10, stock=2, category=tech),
            Book(title="Gamma", price_vnd=5, stock=3, category=tech),
            Book(title="Delta", price_vnd=7, stock=4, category=news),
        ])
        db.session.commit()

    with app.test_client() as test_client:
        yield test_client


def titles(response):
    return [book["title"] for book in response.get_json()["data"]]


def test_offset_pagination(client):
    body = client.get("/api/v1/books?strategy=offset&offset=0&limit=2&sort=price_vnd,title").get_json()
    assert [b["title"] for b in body["data"]] == ["Gamma", "Delta"]
    assert body["page"] == {"strategy": "offset", "offset": 0, "limit": 2, "more": True, "next_offset": 2}

    page2 = client.get("/api/v1/books?strategy=offset&offset=2&limit=2&sort=price_vnd,title").get_json()
    assert [b["title"] for b in page2["data"]] == ["Alpha", "Beta"]
    assert page2["page"]["more"] is False
    assert page2["page"]["next_offset"] is None


def test_cursor_pagination_has_no_duplicates(client):
    first = client.get("/api/v1/books?strategy=cursor&limit=2&sort=price_vnd,title").get_json()
    assert [b["title"] for b in first["data"]] == ["Gamma", "Delta"]
    assert first["page"]["more"] is True

    second = client.get(
        f"/api/v1/books?strategy=cursor&limit=2&sort=price_vnd,title&cursor={first['page']['next']}"
    ).get_json()
    assert [b["title"] for b in second["data"]] == ["Alpha", "Beta"]

    seen = [b["id"] for b in first["data"] + second["data"]]
    assert len(seen) == len(set(seen))


def test_cursor_rejects_tampered_cursor(client):
    assert client.get("/api/v1/books?strategy=cursor&cursor=not-a-real-cursor").status_code == 400
    # cursor hợp lệ nhưng sort khác -> phải bị từ chối
    first = client.get("/api/v1/books?strategy=cursor&limit=2&sort=price_vnd,title").get_json()
    assert client.get(
        f"/api/v1/books?strategy=cursor&sort=-id&cursor={first['page']['next']}"
    ).status_code == 400


def test_genre_filter(client):
    assert titles(client.get("/api/v1/books?genre=tech&sort=price_vnd,title")) == ["Gamma", "Alpha", "Beta"]
    assert titles(client.get("/api/v1/books?genre=news&sort=price_vnd,title")) == ["Delta"]
    # khớp theo tên category, không chỉ slug
    assert titles(client.get("/api/v1/books?genre=News&sort=price_vnd,title")) == ["Delta"]


def test_multi_key_sort_uses_secondary_key(client):
    # Alpha và Beta cùng price_vnd=10 -> title phải quyết định thứ tự
    assert titles(client.get("/api/v1/books?sort=price_vnd,title")) == ["Gamma", "Delta", "Alpha", "Beta"]
    assert titles(client.get("/api/v1/books?sort=-price_vnd,title")) == ["Alpha", "Beta", "Delta", "Gamma"]


def test_invalid_params_rejected(client):
    assert client.get("/api/v1/books?sort=password").status_code == 400
    assert client.get("/api/v1/books?strategy=bogus").status_code == 400
    assert client.get("/api/v1/books?limit=0").status_code == 400
    assert client.get("/api/v1/books?strategy=offset&offset=-1").status_code == 400

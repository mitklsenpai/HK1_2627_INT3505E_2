from pathlib import Path

from flask import Flask

from models import db
from routes.books import books_bp

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{(INSTANCE_DIR / 'bookstore.db').as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(books_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
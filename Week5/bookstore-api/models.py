from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


book_authors = db.Table(
    "book_authors",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id"), primary_key=True)
)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), nullable=True)
    price_vnd = db.Column(db.Integer, nullable=True)
    stock = db.Column(db.Integer, nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    category = db.relationship("Category", back_populates="books")
    authors = db.relationship(
        "Author",
        secondary=book_authors,
        back_populates="books"
    )
    reviews = db.relationship("Review", back_populates="book")

    @classmethod
    def from_payload(cls, payload):
        book = cls()
        book.title = payload.get("title")
        book.isbn = payload.get("isbn")
        book.price_vnd = payload.get("price_vnd")
        book.stock = payload.get("stock")
        return book

    def to_dict(self):
        return {
            "id": f"book_{self.id}",
            "title": self.title,
            "isbn": self.isbn,
            "price_vnd": self.price_vnd,
            "stock": self.stock,
            "category_id": self.category_id
        }


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    books = db.relationship(
        "Book",
        secondary=book_authors,
        back_populates="authors"
    )


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)

    books = db.relationship("Book", back_populates="category")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)

    reviews = db.relationship("Review", back_populates="user")


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    book = db.relationship("Book", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")
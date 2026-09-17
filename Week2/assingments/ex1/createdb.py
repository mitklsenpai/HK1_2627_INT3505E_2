import sqlite3 as sql

connect = sql.connect("Week2/assingments/ex1/dump_database.bd")

connect.execute("""
    create table books (
        id integer primary key,
        title text,
        author text,
        isbn text,
        price real
    )
""")

connect.execute("""
    insert into books (id, title, author, isbn, price) values
        (1, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 10),
        (2, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', 11),
        (3, '1984', 'George Orwell', '9780451524935', 9),
        (4, 'Animal Farm', 'George Orwell', '9780451526342', 8),
        (5, 'Pride and Prejudice', 'Jane Austen', '9780141439518', 12),
        (6, 'The Hobbit', 'J. R. R. Tolkien', '9780547928227', 14)
""")

connect.commit()
connect.close()
"""
Library Management System

A Flask application for managing books and authors in a library. It includes
features to add, search, sort, and delete books, as well as add authors to the database.

Modules:
- `data_models`: Contains SQLAlchemy models for `Author` and `Book`.
"""

import os
from datetime import datetime
from data_models import db, Author, Book
from flask import Flask, flash, render_template, request, redirect

# Define paths for database setup
MAIN_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = "./data"
DB_NAME = "library.sqlite"
DB_PATH = os.path.join(MAIN_FOLDER_PATH, DB_PATH, DB_NAME)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
db.init_app(app)

# Create database if it doesn't exist
if not os.path.exists(DB_PATH):
    with app.app_context():
        db.create_all()
        print("New DB Created")


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home route to display the list of books.

    Allows sorting of books by title, publication year, or author name.
    Handles sorting requests via POST.

    Returns:
        Rendered HTML template with the list of books and sorting choice.
    """
    choice = 'title'
    if request.method == "POST":
        try:
            choice = request.form.get('sorting')
        except Exception as e:
            print(f"Error: {e}")
            return None
    return render_template('home.html', books=get_books_from_db(choice), order=choice)


@app.route('/search', methods=['POST'])
def search_book():
    """
    Search for books by title.

    Handles search requests via POST. Redirects to the home page if no search key is provided.

    Returns:
        Rendered HTML template with the search results or a redirect to the home page.
    """
    if request.method == "POST":
        try:
            search_key = request.form.get('key')
            if not search_key.strip():
                return redirect('/')
            return render_template('home.html', books=get_books_by_title(search_key))
        except Exception as e:
            print(f"Error: {e}")
            return None
    return None


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Add a new author to the database.

    Handles both GET and POST requests. On POST, the form data is used to create a new author.

    Returns:
        Rendered HTML template for adding an author or a notification page after adding.
    """
    if request.method == 'POST':
        new_author = add_author_to_db()
        return render_template("notification.html",
                               obj=new_author, obj_type=type(new_author).__name__)
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book to the database.

    Handles both GET and POST requests. On POST, the form data is used to create a new book.

    Returns:
        Rendered HTML template for adding a book or a notification page after adding.
    """
    if request.method == 'POST':
        new_book = add_book_to_db()
        return render_template("notification.html",
                               obj=new_book, obj_type=type(new_book).__name__)

    authors = get_authors_from_db()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book from the database by its ID.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        Redirects to the home page after deletion.
    """
    delete_book_by_id(book_id)
    return redirect('/')


def add_author_to_db():
    """
    Add a new author to the database using form data.

    Returns:
        Author: The newly created Author object, or None if creation fails.
    """
    author_name = request.form.get('name')
    author_birthdate = request.form.get('birthdate')
    author_date_of_death = request.form.get('date_of_death')

    if not author_name:
        return None

    try:
        birth_date = (
            datetime.strptime(author_birthdate, "%Y-%m-%d").date()
            if author_birthdate else None
        )
        death_date = (
            datetime.strptime(author_date_of_death, "%Y-%m-%d").date()
            if author_date_of_death else None
        )

        new_author = Author(
            name=author_name,
            birth_date=birth_date,
            date_of_death=death_date,
        )
        db.session.add(new_author)
        db.session.commit()
        print('A new author has been successfully added to the database')
        return new_author
    except Exception as e:
        print(f"Error: {e}")
        return None


def add_book_to_db():
    """
    Add a new book to the database using form data.

    Returns:
        Book: The newly created Book object, or None if creation fails.
    """
    book_isbn = request.form.get('isbn')
    book_title = request.form.get('title')
    book_publication_year = request.form.get('publication_year')
    author_id = request.form.get('author')

    if not (book_title or author_id):
        return None

    try:
        publication_year = (
            datetime.strptime(book_publication_year, "%Y-%m-%d").date()
            if book_publication_year else None
        )
        new_book = Book(
            isbn=book_isbn,
            title=book_title,
            publication_year=publication_year,
            author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        print('A new book has been successfully added to the database')
        return new_book
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_authors_from_db(order='name'):
    """
    Fetch all authors from the database.

    Args:
        order (str): The attribute to order authors by. Default is 'name'.

    Returns:
        List[Author]: A list of authors ordered by the specified attribute.
    """
    authors = Author.query.order_by(order)
    return authors


def get_books_from_db(order='title'):
    """
    Fetch all books from the database.

    Args:
        order (str): The attribute to order books by. Can be 'title', 'publication_year', or 'author'.

    Returns:
        List[Book]: A list of books ordered by the specified attribute.
    """
    if order == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(getattr(Book, order)).all()
    return books


def get_books_by_title(title):
    """
    Search for books by their title.

    Args:
        title (str): The title or part of the title to search for.

    Returns:
        List[Book]: A list of books matching the title search query.
    """
    if title:
        try:
            return Book.query.filter(Book.title.like(f"%{title}%")).all()
        except Exception as e:
            print(f"Error: {e}")
            return None


def delete_book_by_id(book_id):
    """
    Delete a book from the database by its ID.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        None
    """
    try:
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash('Book successfully deleted!', 'success')
        print('A book has been successfully deleted from the database')
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

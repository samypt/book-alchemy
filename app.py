import os
from datetime import datetime
from data_models import db, Author, Book
from flask import Flask, flash, render_template, request, url_for, redirect


MAIN_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = "./data"
DB_NAME = "library.sqlite"
DB_PATH = os.path.join(MAIN_FOLDER_PATH, DB_PATH, DB_NAME)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
db.init_app(app)

if not os.path.exists(DB_PATH):
    with app.app_context():
        db.create_all()
        print("New DB Created")


@app.route('/', methods=['GET', 'POST'] )
def home():
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
    if request.method == 'POST':
        new_author = add_author_to_db()
        return render_template("notification.html",
                               obj=new_author, obj_type=type(new_author).__name__)
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = add_book_to_db()
        return render_template("notification.html",
                               obj=new_book, obj_type=type(new_book).__name__)

    authors = get_authors_from_db()
    return render_template('add_book.html', authors = authors)


def add_author_to_db():
    author_name = request.form.get('name')
    author_birthdate = request.form.get('birthdate')
    author_date_of_death = request.form.get('date_of_death')

    # Validate inputs
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

        # Create and add the new author
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
    authors = Author.query.order_by(order)
    return authors


def get_books_from_db(order='title'):
    if order == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(getattr(Book, order)).all()
    return books


def get_books_by_title(title):
    if title:
        try:
            books = Book.query.filter(Book.title.like(f"%{title}%")).all()
            print(books)
            return books
        except Exception as e:
            print(f"Error: {e}")
            return None




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
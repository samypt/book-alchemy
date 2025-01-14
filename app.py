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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        new_author = add_author_to_db()
        return render_template("notification.html", obj=new_author)
    return render_template('add_author.html')


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
            author_name=author_name,
            author_birth_date=birth_date,
            author_date_of_death=death_date,
        )
        db.session.add(new_author)
        db.session.commit()
        print('A new author has been successfully added to the database')
        return new_author
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
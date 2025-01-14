import os
from data_models import Author, Book, db
from flask import Flask, flash, render_template, request


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
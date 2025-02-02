from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)
    # Relationship
    books = db.relationship('Book', backref='author', lazy=True)

    def __str__(self):
        return  f"Author: {self.name} with id : {self.id} has been successfully added to the database"

    def __repr__(self):
        return (f"Author (id = {self.id}, name = {self.author_name}, "
                f"bd = {self.birth_date}, dd = {self.date_of_death})")


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Date, nullable=True)
    # Foreign Key to Author
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    # Relationship
    # author = db.relationship('Author', backref='books')

    def __str__(self):
        return  f"Book: {self.title} with id : {self.id} has been successfully added to the database"


    def __repr__(self):
        return (f"Book (id = {self.id}, title = {self.title}, "
                f"isbn = {self.isbn}, pby = {self.publication_year}, "
                f"aut_id = {self.author_id}, author = {self.author})")

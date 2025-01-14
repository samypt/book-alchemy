from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String, nullable=False)
    author_birth_date = db.Column(db.Date, nullable=True)
    author_date_of_death = db.Column(db.Date, nullable=True)
    # Relationship
    book = db.relationship('Book', backref='authors')

    def __repr__(self):
        return (f"Author (id = {self.author_id}, name = {self.author_name}, "
                f"bd = {self.author_birth_date}, dd = {self.author_date_of_death})")


class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_isbn = db.Column(db.String, nullable=False)
    book_title = db.Column(db.String, nullable=False)
    book_publication_year = db.Column(db.Date, nullable=True)
    # Foreign Key to Author
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
    # Relationship
    author = db.relationship('Author', backref='books')

    def __repr__(self):
        return (f"Book (id = {self.book_id}, title = {self.book_title}, "
                f"isbn = {self.book_isbn}, pby = {self.book_publication_year}, "
                f"aut_id = {self.author_id}, author = {self.author})")

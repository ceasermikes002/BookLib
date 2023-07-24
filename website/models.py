from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Intermediate table for the many-to-many relationship
cart_books = db.Table(
    'cart_books',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    fullname = db.Column(db.String(150))
    username = db.Column(db.String(150))
    carts = db.relationship('Cart', backref='user')
    # Remove books relationship from here

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    book_category = db.relationship('Book', backref='books_category')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    title = db.Column(db.String(100))
    authors = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    cover_image = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    category_rel = db.relationship(Category, overlaps="book_category,books_category")

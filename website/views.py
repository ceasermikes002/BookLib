
from flask import Blueprint, render_template, request, session,jsonify,redirect,flash
from flask_login import login_required, current_user
from .models import Category, Book, User
from . import db
from .models import Category, Book, User, Cart
import requests
from flask import request, jsonify
from sqlalchemy import or_


views = Blueprint('views', __name__)

# ...
@views.route('/')
def landing():
    return render_template('landing.html', user=current_user)

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')


@views.route('/home')
@login_required
def home():
    categories = ['fiction', 'fantasy', 'romance', 'mystery', 'science fiction', 'history', 'biography', 'self-help', 'business', 'travel', 'cookbooks', 'art', 'thriller', 'humor', 'horror', 'children', 'young adult', 'philosophy', 'religion', 'sports', 'science', 'technology', 'politics', 'education', 'health & fitness']
    selected_category = request.args.get('selected_category', 'fiction')

    # fetch_books(categories)

    # Retrieve the user's information from the database using the current_user object
    user = User.query.get(current_user.id)

    if user:
        # Pass the user's username to the template
        username = user.username
    else:
        username = None

    # Fetch books from the database instead of the API
    books = fetch_books_from_database(selected_category)

    return render_template('home.html', books=books, categories=categories, selected_category=selected_category, username = username)

def fetch_books_from_database(category):
    # Retrieve books from the database based on the selected category
    db_category = Category.query.filter_by(name=category).first()
    if db_category:
        books = Book.query.filter_by(category_id=db_category.id).all()
        # Convert the list of books to a dictionary with 'category' as the key
        books_dict = {category: books}
        return books_dict
    else:
        return {}

api_key = 'AIzaSyBJaOuBu-R6Z3coZcvV-0V1rZZmJdPTMn0'

# def fetch_books(categories, max_results=40):
#     url = 'https://www.googleapis.com/books/v1/volumes'
#     all_books = {}

#     for category in categories:
#         db_category = Category.query.filter_by(name=category).first()
#         if not db_category:
#             db_category = Category(name=category)
#             db.session.add(db_category)
#             db.session.commit()

#         params = {
#             'q': f'subject:{category}',
#             'maxResults': max_results,
#             'key': api_key
#         }

#         response = requests.get(url, params=params)
#         data = response.json()

#         if 'items' in data:
#             books = data['items']
#             category_books = []

#             for book in books:
#                 volume_info = book['volumeInfo']
#                 title = volume_info.get('title')
#                 authors = volume_info.get('authors')
#                 description = volume_info.get('description')
#                 cover_image = volume_info.get('imageLinks', {}).get('thumbnail')

#                 book_info = {
#                     'title': title,
#                     'authors': authors,
#                     'description': description,
#                     'cover_image': cover_image,
#                 }
#                 category_books.append(book_info)

                
#                 # Check if a book with the same title already exists in the database
#                 existing_book = Book.query.filter_by(title=title).first()

#                 if existing_book:
#                     print(f"Book '{title}' already exists in the database. Skipping...")
#                     continue

#                 # Convert authors list to a comma-separated string
#                 authors_str = ', '.join(authors) if authors else None

#                 book_instance = Book(
#                     category=db_category.name,  # Use the category name instead of the Category object
#                     title=title,
#                     authors=authors_str,
#                     description=description,
#                     cover_image=cover_image,
#                     category_id=db_category.id 
#                 )

#                 db.session.add(book_instance)
#                 db.session.commit()

#             all_books[category] = category_books

#         else:
#             print(f'No books found for the category: {category}')

#     return all_books

# Cart Route
@views.route('/cart')
def cart():
    # Retrieve the user's cart
    user = User.query.get(current_user.id)
    cart = user.carts[-1] if user.carts else None

    if cart and cart.data:
        cart_books = cart.data.split('\n')
    else:
        cart_books = None

    return render_template('cart.html', cart_books=cart_books)


# wishlist Route
@views.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

# checkout Route
@views.route('/checkout')
def checkout():
    return render_template('checkout.html')

# Route for handling adding books to cart
@views.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    if request.method == 'POST':
        book_data = request.get_json()
        book_title = book_data.get('title')
        book_authors = book_data.get('authors')
        book_cover = book_data.get('cover')
        book_price = book_data.get('price')

        # Get the current user's cart or create a new one if it doesn't exist
        user = User.query.get(current_user.id)
        cart = user.carts[-1] if user.carts else None

        if not cart:
            # Create a new cart for the user if it doesn't exist
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)

        # Append the book information to the cart's data
        cart.data = f"{cart.data}\nTitle: {book_title}, Authors: {book_authors}, Cover: {book_cover}, Price: {book_price}"
        db.session.commit()

        flash('Book added to cart successfully', category='success')

    return jsonify({'message': 'Book added to cart successfully'})


# item count route
@views.route('/cart_item_count')
def cart_item_count():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        cart = user.carts[-1] if user.carts else None
        if cart:
            item_count = len(cart.books)
        else:
            item_count = 0
    else:
        item_count = 0
    return jsonify({'count': item_count})
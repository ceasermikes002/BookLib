from flask import Blueprint, render_template,request,flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')

        

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category= 'error')   
        else:
            flash('Email does not exist.', category='error')         

              # Debug statements
        if user is None:      
            print(f"Email: {email}")
            print(f"Password: {password}")
            print(f"User: {user}")

    return render_template('./login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(fullname.split()) < 2:
            flash('Enter your proper fullname!', category='error')
        elif password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 7:
            flash('Password is too short, it should be at least 7 characters!', category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                new_user = User(email=email, fullname=fullname, username=username, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('User already exists.', category='error')
                return redirect(url_for('auth.login'))

    return render_template('./sign-up.html', user=current_user)


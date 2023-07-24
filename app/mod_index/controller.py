# app/mod_index/controller.py
from . import mod_index
from flask import render_template, request, redirect, url_for, flash, session
# from config import db
from app import db

# from app import app, db
from app.models.login import User


@mod_index.route('/')
def index():
    # Check if the database is connected
    db_status = "Connected" if db.engine else "Not Connected"
    
    return render_template('index.html', db_status=db_status)


@mod_index.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Check if the username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', category = 'danger')
            return redirect(url_for('mod_index.register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('mod_index.register'))

        # Create a new user and add to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('mod_index.login'))
    return render_template('register.html')

# app/routes.py


@mod_index.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match a user in the database
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Log the user in by storing their user ID in the session
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('mod_index.index'))

        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('mod_index.login'))

    return render_template('login.html')

@mod_index.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('mod_index.logout'))
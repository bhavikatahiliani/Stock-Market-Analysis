# app/__init__.py
from flask import Flask
from config import db, SQLALCHEMY_DATABASE_URI

def create_app():
    app = Flask(__name__)

    # Load the app configuration from config.py
    app.config.from_object('config')

    # Update the SQLALCHEMY_DATABASE_URI directly
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    # Initialize the database
    db.init_app(app)

    # Register the blueprint for mod_index
    from .mod_index import mod_index
    app.register_blueprint(mod_index)

    return app


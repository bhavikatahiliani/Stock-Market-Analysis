# app/__init__.py
from flask import Flask
from config import db, SQLALCHEMY_DATABASE_URI

def create_app():
    app = Flask(__name__)

    # Load the app configuration from config.py
    app.config.from_object('config')

    # Update the SQLALCHEMY_DATABASE_URI directly
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    app.config['SECRET_KEY'] = 'asdjfls978578!l'

    # Initialize the database
    db.init_app(app)

    # Register the blueprints
    from .mod_index import mod_index
    from .mod_trade import mod_trade
    app.register_blueprint(mod_index)
    app.register_blueprint(mod_trade)

    return app


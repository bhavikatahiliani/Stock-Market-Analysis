# app/mod_trade/__init__.py
from flask import Blueprint

mod_trade = Blueprint('mod_trade', __name__, url_prefix='/trade')

# Import the controller to register the routes
from . import controller

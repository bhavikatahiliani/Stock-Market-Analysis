#app/mod_index/__init__.py file
from flask import Blueprint

# Create the blueprint object with a non-empty name
mod_index = Blueprint('mod_index', __name__, url_prefix='/')

# Import the controller to register the routes
from . import controller

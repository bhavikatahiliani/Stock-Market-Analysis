#stock_market/manage.py
from flask_migrate import Migrate
from flask import Flask
from app import create_app, db

app = create_app()  # Replace 'your_app' with the name of your Flask app
migrate = Migrate(app, db)

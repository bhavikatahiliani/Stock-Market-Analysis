# config.py
from flask_sqlalchemy import SQLAlchemy

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'root'
POSTGRES_DB = 'Stocks'
POSTGRES_HOST = 'localhost'  # Change this to your PostgreSQL host if it's different
POSTGRES_PORT = '5432'  # Change this to your PostgreSQL port if it's different

# Replace 'your_database_uri_here' with the actual PostgreSQL database URI
DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Flask SQLAlchemy configuration
db = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

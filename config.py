# config.py
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
import os

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'root'
POSTGRES_DB = 'Stocks'
POSTGRES_HOST = 'localhost'  # Change this to your PostgreSQL host if it's different
POSTGRES_PORT = '5432'  # Change this to your PostgreSQL port if it's different

# Replace 'your_database_uri_here' with the actual PostgreSQL database URI
DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
# postgresql://stocks_4h01_user:V6Ky84s4OQ0VfWDU2VG1B42wGz2k3VTt@dpg-cjhndmt1a6cs73eek3eg-a.oregon-postgres.render.com/stocks_4h01

# Flask SQLAlchemy configuration
db = SQLAlchemy()
# SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

Base = declarative_base()

def create_user_table():
    engine = create_engine(DATABASE_URI)
    metadata = MetaData()
    Base.metadata.create_all(engine, checkfirst=True)

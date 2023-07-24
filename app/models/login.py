# app/models/login.py

from app import db
from sqlalchemy import Column, Integer, String


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f'User(user_id:{self.id}, user_name: {self.username}, email: {self.email}, password: {self.password})'


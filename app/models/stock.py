# app/models/stock.py

from app import db
from sqlalchemy import Column, Integer, String

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'Stock(id: {self.id}, name: {self.name}, symbol: {self.symbol})'
    
    

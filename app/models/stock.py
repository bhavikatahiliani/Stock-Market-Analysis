# app/models/stock.py

from app import db
from sqlalchemy import Column, Integer, String

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(20), unique=True, nullable=False)
    # price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'Stock(id: {self.id}, name: {self.name}, symbol: {self.symbol})'
    

    @staticmethod
    def create_stock(name, symbol):
        stock = Stock(name=name, symbol=symbol)
        db.session.add(stock)
        db.session.commit()

    @staticmethod
    def update_stock(stock_id, name, symbol):
        stock = Stock.query.get(stock_id)
        if stock:
            stock.name = name
            stock.symbol = symbol
            db.session.commit()

    @staticmethod
    def delete_stock(stock_id):
        stock = Stock.query.get(stock_id)
        if stock:
            db.session.delete(stock)
            db.session.commit()

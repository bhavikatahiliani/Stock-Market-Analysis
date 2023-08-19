# app/models/trade.py
from app import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Trade(db.Model):
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    stock_id = db.Column(db.Integer, ForeignKey('stock.id'), nullable=False)
    stock_symbol = db.Column(db.String(20), nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)  # 'BUY' or 'SELL'
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    trade_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='trades')
    # stock = relationship('Stock', back_populates='trades')

    def __repr__(self):
        return f'Trade(id: {self.id}, user_id: {self.user_id}, stock_id: {self.stock_id}, ' \
               f'stock_symbol: {self.stock_symbol}, trade_type: {self.trade_type}, ' \
               f'quantity: {self.quantity}, amount: {self.amount}, trade_date: {self.trade_date})'

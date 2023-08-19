# app/mod_trade/controller.py
from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models.trade import Trade
from app.models.stock import Stock
from app.models.login import User
from datetime import datetime
# from flask_login import  current_user
from app.mod_trade import mod_trade
from yahoo_fin import stock_info
import matplotlib.pyplot as plt



# @mod_trade.route('/')
# def trade():
#     stocks = Stock.query.all()
#     return render_template('trade.html', stocks=stocks)

@mod_trade.route('/')
def trade():
    try:
        # Fetch stock symbols from the database
        stocks = Stock.query.all()

        stock_symbols = [stock.symbol for stock in stocks]

        # Fetch live stock data for each symbol using yahoo_fin
        live_stock_data = {}
        for stock_symbol in stock_symbols:
            try:
                print(stock_symbol)
                live_price = stock_info.get_live_price(stock_symbol)
                live_stock_data[stock_symbol] = live_price
            except Exception as e:
                print(f"Error fetching stock data for {stock_symbol} using yahoo_fin: {e}")
                live_stock_data[stock_symbol] = None

        return render_template('trade.html', stocks=stocks, live_stock_data=live_stock_data)
    except Exception as e:
        print(f"Error fetching live stocks: {e}")
        return "Error fetching live stocks"

# current_user = "bhavi" 
# balance = 1000
# @mod_trade.route('/')
# # @login_required
# def trade():
#     stocks = Stock.query.all()
#     # trades = Trade.query.filter_by(user_id=current_user).all()
#     return render_template('trade.html', stocks=stocks)

@mod_trade.route('/buy/<int:stock_id>', methods=['GET', 'POST'])
def buy(stock_id):
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        stock = Stock.query.get(stock_id)
        if stock:
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            price = stock_info.get_live_price(stock.symbol)

            if user and quantity > 0:
                trade = Trade(user_id=user_id, stock_id=stock.id, stock_symbol=stock.symbol, trade_type='BUY',
                              quantity=quantity, amount=price * quantity, trade_date=datetime.utcnow())
                db.session.add(trade)
                db.session.commit()
                flash(f'Bought {quantity} shares of {stock.symbol}.', 'success')
            else:
                flash('Invalid user or quantity.', 'danger')

            return redirect(url_for('mod_trade.trade'))
    return render_template('trade_form.html', action='Buy')



# @mod_trade.route('/buy/<int:stock_id>', methods=['POST'])
# # @login_required 
# def buy(stock_id):
#     quantity = int(request.form['quantity'])
#     stock = Stock.query.get(stock_id)

#     if stock:
#         # Fetch the current price of the stock from the fetch_live_stocks() function in app/mod_index/controller.py
#         current_price = stock_info.get_live_price(stock.symbol)

#         if current_price is None:
#             flash(f"Failed to get the current price of {stock.name} ({stock.symbol}). Please try again later.", 'error')
#             return redirect(url_for('trade.trade'))

#         total_amount = current_price * quantity
#         if balance >= total_amount:
#             # Update the user balance and create a trade record
#             balance -= total_amount
#             trade = Trade(user_id=current_user.id, stock_id=stock_id, quantity=quantity, amount=total_amount, trade_date=datetime.utcnow())
#             db.session.add(trade)
#             db.session.commit()
#             flash(f"Successfully bought {quantity} shares of {stock.name} ({stock.symbol}) for ${total_amount:.2f}.", 'success')
#         else:
#             flash("Insufficient balance to make the purchase.", 'error')
#     else:
#         flash("Stock not found.", 'error')

#     return redirect(url_for('trade.trade'))

@mod_trade.route('/sell/<int:stock_id>', methods=['GET', 'POST'])
def sell(stock_id):
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        stock = Stock.query.get(stock_id)
        print(stock)
        print(stock)
        print(stock)
        if stock:
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            price = stock_info.get_live_price(stock.symbol)

            if user and quantity > 0:
                trade = Trade(user_id=user_id, stock_id=stock.id, stock_symbol=stock.symbol, trade_type='SELL',
                              quantity=quantity, amount = price * quantity, trade_date=datetime.utcnow())
                db.session.add(trade)
                db.session.commit()
                flash(f'Sold {quantity} shares of {stock.symbol}.', 'success')
            else:
                flash('Invalid user or quantity.', 'danger')

            return redirect(url_for('mod_trade.trade'))
    return render_template('trade_form.html', action='Sell')



# @mod_trade.route('/sell/<int:trade_id>', methods=['POST'])
# # @login_required
# def sell(trade_id):
#     trade = Trade.query.get(trade_id)

#     if trade:
#         stock = trade.stock
#         # Fetch the current price of the stock from the fetch_live_stocks() function in app/mod_index/controller.py
#         current_price = stock_info.get_live_price(stock.symbol)

#         if current_price is None:
#             flash(f"Failed to get the current price of {stock.name} ({stock.symbol}). Please try again later.", 'error')
#             return redirect(url_for('trade.trade'))

#         total_amount = current_price * trade.quantity
#         balance += total_amount
#         db.session.delete(trade)
#         db.session.commit()
#         flash(f"Successfully sold {trade.quantity} shares of {stock.name} ({stock.symbol}) for ${total_amount:.2f}.", 'success')
#     else:
#         flash("Trade not found.", 'error')

#     return redirect(url_for('trade.trade'))




# @mod_trade.route('/portfolio')
# def portfolio():
#     user_id = session.get('user_id')
#     if user_id is None:
#         flash('Please login to view your portfolio.', 'danger')
#         return redirect(url_for('mod_index.login'))

#     # Query the user's trades
#     user_trades = Trade.query.filter_by(user_id=user_id).all()

#     # Create a dictionary to store the user's portfolio data
#     portfolio_data = {}

#     # Calculate the portfolio
#     for trade in user_trades:
#         stock_symbol = trade.stock_symbol
#         quantity = trade.quantity
#         current_price = stock_info.get_live_price(stock_symbol)
#         total_value = quantity * current_price

#         if stock_symbol in portfolio_data:
#             portfolio_data[stock_symbol]['quantity'] += quantity
#             portfolio_data[stock_symbol]['total_value'] += total_value
#         else:
#             portfolio_data[stock_symbol] = {
#                 'quantity': quantity,
#                 'current_price': current_price,
#                 'total_value': total_value
#             }

#     return render_template('portfolio.html', portfolio_data=portfolio_data)




# @mod_trade.route('/portfolio')
# def portfolio():
#     user_id = session.get('user_id')
#     if user_id is None:
#         flash('Please login to view your portfolio.', 'danger')
#         return redirect(url_for('mod_index.login'))

#     # Query the user's trades
#     user_trades = Trade.query.filter_by(user_id=user_id).all()

#     # Create a dictionary to store the user's portfolio data
#     portfolio_data = {}

#     # Calculate the portfolio
#     for trade in user_trades:
#         stock_symbol = trade.stock_symbol
#         quantity = trade.quantity
#         current_price = stock_info.get_live_price(stock_symbol)
#         total_value = quantity * current_price

#         if stock_symbol in portfolio_data:
#             portfolio_data[stock_symbol]['quantity'] += quantity
#             portfolio_data[stock_symbol]['total_value'] += total_value
#         else:
#             portfolio_data[stock_symbol] = {
#                 'quantity': quantity,
#                 'current_price': current_price,
#                 'total_value': total_value
#             }

#     # Extract data for the graph
#     stock_symbols = list(portfolio_data.keys())
#     portfolio_values = [data['total_value'] for data in portfolio_data.values()]

#     # Create a bar chart
#     plt.figure(figsize=(10, 6))
#     plt.bar(stock_symbols, portfolio_values)
#     plt.xlabel('Stock Symbol')
#     plt.ylabel('Total Value')
#     plt.title('Portfolio Value by Stock Symbol')
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     # Save the chart to a file or render it in the template
#     # You can save it to a file like this:
#     # plt.savefig('portfolio_chart.png')

#     # Or render it in the template like this:
#     # portfolio_chart = plt_to_img(plt)  # Assuming you have a function to convert plt to an image

#     # Return the chart to the template
#     # return render_template('portfolio.html', portfolio_data=portfolio_data, portfolio_chart=portfolio_chart)
    
#     # For this example, I'm saving the chart to a file
#     plt.savefig('portfolio_chart.png')
    
#     return render_template('portfolio.html', portfolio_data=portfolio_data)


import io
import base64

# ... (other imports and route definitions)

@mod_trade.route('/portfolio')
def portfolio():
    user_id = session.get('user_id')
    if user_id is None:
        flash('Please login to view your portfolio.', 'danger')
        return redirect(url_for('mod_index.login'))

    # Query the user's trades
    user_trades = Trade.query.filter_by(user_id=user_id).all()

    # Create a dictionary to store the user's portfolio data
    portfolio_data = {}

    # Calculate the portfolio
    for trade in user_trades:
        stock_symbol = trade.stock_symbol
        quantity = trade.quantity
        current_price = stock_info.get_live_price(stock_symbol)
        total_value = quantity * current_price

        if stock_symbol in portfolio_data:
            portfolio_data[stock_symbol]['quantity'] += quantity
            portfolio_data[stock_symbol]['total_value'] += total_value
        else:
            portfolio_data[stock_symbol] = {
                'quantity': quantity,
                'current_price': current_price,
                'total_value': total_value
            }

    # Extract data for the graph
    stock_symbols = list(portfolio_data.keys())
    portfolio_values = [data['total_value'] for data in portfolio_data.values()]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(stock_symbols, portfolio_values)
    plt.xlabel('Stock Symbol')
    plt.ylabel('Total Value')
    plt.title('Portfolio Value by Stock Symbol')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart as an image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as base64
    chart_url = base64.b64encode(img.getvalue()).decode()

    return render_template('portfolio.html', portfolio_data=portfolio_data, portfolio_chart=chart_url)


# app/mod_index/controller.py
from . import mod_index
from flask import render_template, request, redirect, url_for, flash, session
# from config import db
from app import db

# from app import app, db
from app.models.login import User
from app.models.stock import Stock
from yahoo_fin import stock_info
from app.forms import StockForm


@mod_index.route('/index')
def index():
    # Check if the database is connected
    db_status = "Connected" if db.engine else "Not Connected"
    
    return render_template('index.html', db_status=db_status)


@mod_index.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Check if the username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', category = 'danger')
            return redirect(url_for('mod_index.register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('mod_index.register'))

        # Create a new user and add to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('mod_index.login'))
    return render_template('register.html')

# app/routes.py


@mod_index.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match a user in the database
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Log the user in by storing their user ID in the session
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('mod_index.index'))

        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('mod_index.login'))

    return render_template('login.html')

@mod_index.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('mod_index.login'))




# @mod_index.route('/stocks')
# def fetch_live_stocks():
#     try:
#         # Fetch stock symbols from the database
#         stocks = Stock.query.all()
#         print("Stocks:")
#         print(stocks)

#         stock_symbols = [stock.symbol for stock in stocks]

#         # Fetch live stock data for each symbol using jugaad_data.nse and yfinance
#         live_stock_data = {}
#         for stock_symbol in stock_symbols:
#             try:
#                 nse = NSELive()
#                 stock_data = nse.get_quote(stock_symbol)
#                 live_stock_data[stock_symbol] = stock_data['lastPrice']
#             except Exception as e:
#                 print(f"Error fetching NSE data for {stock_symbol} using jugaad_data.nse: {e}")
#                 try:
#                     stock = yf.Ticker(stock_symbol)
#                     stock_data = stock.info
#                     live_stock_data[stock_symbol] = stock_data.get('regularMarketPrice', None)
#                 except Exception as e:
#                     print(f"Error fetching NSE data for {stock_symbol} using yfinance: {e}")
#                     live_stock_data[stock_symbol] = None

#         return render_template('stocks.html', live_stock_data=live_stock_data)
#     except Exception as e:
#         print(f"Error fetching live stocks: {e}")
#         return "Error fetching live stocks"

# app/mod_index/controller.py


# app/mod_index/controller.py


# @mod_index.route('/stocks')
# def fetch_live_stocks():
#     try:
#         # Fetch stock symbols from the database
#         stocks = Stock.query.all()
#         print("Stocks:")
#         print(stocks)

#         stock_symbols = [stock.symbol for stock in stocks]

#         # Fetch live stock data for each symbol using yfinance
#         live_stock_data = {}
#         for stock_symbol in stock_symbols:
#             try:
#                 stock = yf.Ticker(stock_symbol)
#                 stock_data = stock.info
#                 if 'regularMarketPrice' in stock_data:
#                     live_stock_data[stock_symbol] = stock_data['regularMarketPrice']
#                 else:
#                     live_stock_data[stock_symbol] = None
#             except Exception as e:
#                 print(f"Error fetching stock data for {stock_symbol} using yfinance: {e}")
#                 live_stock_data[stock_symbol] = None

#         return render_template('stocks.html', live_stock_data=live_stock_data)
#     except Exception as e:
#         print(f"Error fetching live stocks: {e}")
#         return "Error fetching live stocks"


@mod_index.route('/stocks')
def fetch_live_stocks():
    try:
        # Fetch stock symbols from the database
        stocks = Stock.query.all()
        print("Stocks:")
        print(stocks)

        stock_symbols = [stock.symbol for stock in stocks]

        # Fetch live stock data for each symbol using yahoo_fin
        live_stock_data = {}
        for stock_symbol in stock_symbols:
            try:
                live_price = stock_info.get_live_price(stock_symbol)
                live_stock_data[stock_symbol] = live_price
            except Exception as e:
                print(f"Error fetching stock data for {stock_symbol} using yahoo_fin: {e}")
                live_stock_data[stock_symbol] = None

        return render_template('stocks.html', live_stock_data=live_stock_data)
    except Exception as e:
        print(f"Error fetching live stocks: {e}")
        return "Error fetching live stocks"
    

# app/mod_index/controller.py

# ... (existing code)

# Add a route to display a list of all stocks
@mod_index.route('/stocks/list')
def list_stocks():
    stocks = Stock.query.all()
    return render_template('stock_list.html', stocks=stocks)

@mod_index.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    form = StockForm()
    if form.validate_on_submit():
        name = form.name.data
        symbol = form.symbol.data
        Stock.create_stock(name, symbol)
        flash('Stock added successfully!', 'success')
        return redirect(url_for('mod_index.add_stock'))
    return render_template('add_stock.html', form=form)

@mod_index.route('/edit_stock/<int:stock_id>', methods=['GET', 'POST'])
def edit_stock(stock_id):
    stock = Stock.query.get(stock_id)
    if not stock:
        flash('Stock not found!', 'danger')
        return redirect(url_for('mod_index.edit_stock'))
    form = StockForm(obj=stock)
    if form.validate_on_submit():
        name = form.name.data
        symbol = form.symbol.data
        Stock.update_stock(stock_id, name, symbol)
        flash('Stock updated successfully!', 'success')
        return redirect(url_for('mod_index.edit_stock', stock_id=stock_id))
    return render_template('edit_stock.html', form=form, stock=stock)

# @mod_index.route('/delete_stock/<int:stock_id>', methods=['POST'])
# def delete_stock(stock_id):
#     stock = Stock.query.get(stock_id)
#     if stock:
#         Stock.delete_stock(stock_id)
#         flash('Stock deleted successfully!', 'success')
#     else:
#         flash('Stock not found!', 'danger')
#     return redirect(url_for('mod_index.delete_stock', stock_id=stock_id))

@mod_index.route('/delete_stock/<int:stock_id>', methods=['GET', 'POST'])
def delete_stock(stock_id):
    if request.method == 'POST':
        stock = Stock.query.get(stock_id)
        if stock:
            Stock.delete_stock(stock_id)
            flash('Stock deleted successfully!', 'success')
        else:
            flash('Stock not found!', 'danger')
    
    # Redirect back to the stock list page, for example:
    return redirect(url_for('mod_index.list_stocks'))

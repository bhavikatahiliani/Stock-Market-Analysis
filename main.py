
#stock_market/main.py

from app import create_app, db
# from config import create_user_table
# from config import create_user_table


if __name__ == "__main__":
    app = create_app()

    # with app.app_context():
    #     create_user_table()

    app.run(debug=False)
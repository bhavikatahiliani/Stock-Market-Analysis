# app/mod_index/controller.py
from . import mod_index
from flask import render_template
from config import db

@mod_index.route('/')
def index():
    # Check if the database is connected
    db_status = "Connected" if db.engine else "Not Connected"
    
    return render_template('index.html', db_status=db_status)

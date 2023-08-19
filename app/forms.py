# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    name = StringField('Stock Name', validators=[DataRequired()])
    symbol = StringField('Stock Symbol', validators=[DataRequired()])
    submit = SubmitField('Submit')

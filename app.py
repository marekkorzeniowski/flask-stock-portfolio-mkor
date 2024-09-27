import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, session, redirect, url_for, flash
from markupsafe import escape
from pydantic import BaseModel, field_validator, ValidationError


class StockModel(BaseModel):
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @field_validator('stock_symbol')
    def stock_symbol_check(cls, value: str):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()

# App initialization
app = Flask(__name__)
app.secret_key = 'b635c5db37076f0ffdcb5f09fe1ec9d2a4397b2f1b6943d0b89d6c6397ea3e25'

# Logging Configuration
# Option 1
# file_handler = logging.FileHandler('flask-stock-portfolio.log')
# Option 2
file_handler = RotatingFileHandler('flask-stock-portfolio.log',
                                   maxBytes=16384,
                                   backupCount=20) # max number of files, before start of overwriting
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
app.logger.addHandler(file_handler)
# OPTIONAL - Remove the default logger configured by Flask
# app.logger.removeHandler(default_handler)

# Log that the Flask application is starting
app.logger.info('Starting the Flask Stock Portfolio App...')


@app.route('/')
def index():
    app.logger.info('Calling the index() function.')
    return render_template('index.html')

@app.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('about.html', company_name='Mkor')


@app.route('/hello/<message>')
def hello_message(message):
    return f'<h1>Welcome {escape(message)}!</h1>'

@app.route('/blog_posts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}...</h1>'


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f"{key}: {value}")

        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            # Save data to the session object
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price

            # flash message
            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')
            app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")

            return redirect(url_for('list_stocks'))

        except ValidationError as e:
            print(e)

    return render_template('add_stock.html')


@app.route('/stocks/')
def list_stocks():
    return render_template('stocks.html')

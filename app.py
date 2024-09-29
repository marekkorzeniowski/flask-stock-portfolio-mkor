import logging
from logging.handlers import RotatingFileHandler

from flask import Flask


# App initialization
app = Flask(__name__)
app.secret_key = 'b635c5db37076f0ffdcb5f09fe1ec9d2a4397b2f1b6943d0b89d6c6397ea3e25'


# Import the blueprints
from project.stocks import stocks_blueprint
from project.users import users_blueprint

# Register the blueprints
app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')

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


# @app.route('/hello/<message>')
# def hello_message(message):
#     return f'<h1>Welcome {escape(message)}!</h1>'
#
# @app.route('/blog_posts/<int:post_id>')
# def display_blog_post(post_id):
#     return f'<h1>Blog Post #{post_id}...</h1>'



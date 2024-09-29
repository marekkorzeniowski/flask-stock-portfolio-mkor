import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask


# App initialization
app = Flask(__name__)
# Configure the Flask application
config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(config_type)

# Import the blueprints
from project.stocks import stocks_blueprint
from project.users import users_blueprint

# Register the blueprints
app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')

# Logging Configuration
file_handler = RotatingFileHandler('instances/flask-stock-portfolio.log',
                                   maxBytes=16384,
                                   backupCount=2) # max number of files, before start of overwriting
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
app.logger.addHandler(file_handler)

# Log that the Flask application is starting
app.logger.info('Starting the Flask Stock Portfolio App...')




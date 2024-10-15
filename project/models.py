from datetime import datetime

import flask_login

from project import database
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Stock(database.Model):
    __tablename__ = 'stocks'

    id = mapped_column(Integer(), primary_key=True)
    stock_symbol = mapped_column(String())
    number_of_shares = mapped_column(Integer())
    purchase_price = mapped_column(Integer())
    user_id = mapped_column(ForeignKey('users.id'))
    purchase_date = mapped_column(DateTime())

    # Define the relationship to the `Stock` class
    user_relationship = relationship('User', back_populates='stocks_relationship')

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str,
                 user_id: int, purchase_date=None):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)
        self.user_id = user_id
        self.purchase_date = purchase_date

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} shares purchased at ${self.purchase_price / 100}'


class User(flask_login.UserMixin, database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, unique=True)
    password_hashed = database.Column(database.String(128))
    registered_on = mapped_column(DateTime())                  
    email_confirmation_sent_on = mapped_column(DateTime())     
    email_confirmed = mapped_column(Boolean(), default=False)  
    email_confirmed_on = mapped_column(DateTime())

    # Define the relationship to the `Stock` class
    stocks_relationship = relationship('Stock', back_populates='user_relationship')

    def __init__(self, email: str, password_plaintext: str):
        """Create a new User object

        This constructor assumes that an email is sent to the new user to confirm
        their email address at the same time that the user is registered.
        """
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = datetime.now()
        self.email_confirmed = False
        self.email_confirmed_on = None

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'
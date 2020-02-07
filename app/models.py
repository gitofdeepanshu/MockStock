import base64
import os

from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.ext.associationproxy import association_proxy

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    member1 = db.Column(db.String(64))
    member2 = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    session_token = db.Column(db.String(32), index=True, unique=True)

    stocks = association_proxy('stock_items', 'stock',
                               creator=lambda v: StockItem(stock=v))

    def __init__(self, username, email, member1=None, member2=None):
        self.username = username
        self.email = email
        self.member1 = member1
        self.member2 = member2

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_token(self):
        self.session_token = base64.b64encode(os.urandom(24)).decode('utf-8')
        db.session.add(self)
        return self.session_token

    def revoke_token(self):
        self.session_token = None

    def get_auth_session_token(self):
        return self.session_token


@login.user_loader
def load_user(session_token):
    return User.query.filter_by(session_token=session_token).first()


class Stock(db.Model):
    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(5), unique=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Numeric(13, 2))

    def __repr__(self):
        return f"Stock<{self.symbol}>"


class StockItem(db.Model):
    __tablename__ = "stockitem"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey(
        'stock.id'), primary_key=True)
    quantity = db.Column(db.Integer)

    user = db.relationship(User, backref=db.backref(
        "stock_items",
        cascade="all, delete-orphan",)
    )

    stock = db.relationship("Stock")

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# Association table for many-to-many relationship between User and Crypto Token
watchlist = db.Table('watchlists',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('token_id', db.Integer, db.ForeignKey('tokens.id'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Watchlist
    watchlist = db.relationship('Token', secondary=watchlist, backref=db.backref('users', lazy='dynamic'))

    # Alerts
    alerts = db.relationship('Alert', backref='user', lazy='dynamic')

    # Trades
    trades = db.relationship('Trade', backref='user', lazy='dynamic')

    # Wallet
    wallet = db.relationship('Wallet', backref='user', uselist=False)

class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    symbol = db.Column(db.String(10), index=True, unique=True)

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Float)
    direction = db.Column(db.String(10))  # increase or decrease

    token = db.relationship('Token', backref='alerts')

class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'))
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    time = db.Column(db.DateTime)
    type = db.Column(db.String(10))  # buy or sell
    status = db.Column(db.String(10))  # open or closed
    pnl = db.Column(db.Float)  # profit and loss
    futures = db.Column(db.Boolean)  # true for futures trades, false for spot trades
    order_type = db.Column(db.String(20))  # market, limit, stop limit, stop market, trailing stop, post only, scaled order

    token = db.relationship('Token', backref='trades')


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    balance = db.Column(db.Float)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'))
    amount = db.Column(db.Float)
    transaction_type = db.Column(db.String(10))  # deposit or withdrawal

    wallet = db.relationship('Wallet', backref='transactions')

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        include_fk = True

class TokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Token
        include_relationships = True
        load_instance = True
        include_fk = True

class AlertSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Alert
        include_relationships = True
        load_instance = True
        include_fk = True

class TradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trade
        include_relationships = True
        load_instance = True
        include_fk = True

class WalletSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wallet
        include_relationships = True
        load_instance = True
        include_fk = True

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        include_relationships = True
        load_instance = True
        include_fk = True

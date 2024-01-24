from models import db, User, Token, Alert, Trade, Wallet, Transaction, Price
from datetime import datetime
from services import BinanceService
from app import app

def seed_data():
    try:
        # Will add some data here
        user1 = User.query.filter_by(username='user1', email='user1@example.com').first()
        if not user1:
            user1 = User(username='user1', email='user1@example.com')
            user1.set_password('password123')
            db.session.add(user1)

        token1 = Token.query.filter_by(name='Bitcoin', symbol='BTCUSDT').first()
        if not token1:
            token1 = Token(name='Bitcoin', symbol='BTCUSDT')
            db.session.add(token1)

        alert1 = Alert.query.filter_by(user_id=1, token_id=1, price=50000, direction='increase').first()
        if not alert1:
            alert1 = Alert(user_id=1, token_id=1, price=50000, direction='increase')
            db.session.add(alert1)

        trade1 = Trade.query.filter_by(user_id=1, token_id=1, amount=0.01, price=50000, time=datetime.strptime('2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), type='buy', status='open', pnl=0, futures=False, order_type='market').first()  # spot market order to buy 0.01 BTC at $50,000
        if not trade1:
            trade1 = Trade(user_id=1, token_id=1, amount=0.01, price=50000, time=datetime.strptime('2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), type='buy', status='open', pnl=0, futures=False, order_type='market')  # spot market order to buy 0.01 BTC at $50,000
            db.session.add(trade1)

        trade2 = Trade.query.filter_by(user_id=1, token_id=1, amount=0.01, price=60000, time=datetime.strptime('2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), type='buy', status='open', pnl=0, futures=True, order_type='limit').first()  # futures limit order to buy 0.01 BTC at $60,000
        if not trade2:
            trade2 = Trade(user_id=1, token_id=1, amount=0.01, price=60000, time=datetime.strptime('2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), type='buy', status='open', pnl=0, futures=True, order_type='limit')  # futures limit order to buy 0.01 BTC at $60,000
            db.session.add(trade2)

        wallet1 = Wallet.query.filter_by(user_id=1, balance=100000).first()
        if not wallet1:
            wallet1 = Wallet(user_id=1, balance=100000)
            db.session.add(wallet1)

        transaction1 = Transaction.query.filter_by(wallet_id=1, amount=100000, transaction_type='deposit').first()  # Initial deposit
        if not transaction1:
            transaction1 = Transaction(wallet_id=1, amount=100000, transaction_type='deposit')  # Initial deposit
            db.session.add(transaction1)
        
        service = BinanceService()
        price = service.get_price('BTCUSDT')
        token = Token.query.filter_by(symbol='BTCUSDT').first()
        if token:
            price_entry = Price(token_id=token.id, price=price)
            db.session.add(price_entry)


        db.session.commit()
        print("Data seeding successful!")
    except Exception as e:
        print(f"An error occurred while seeding data: {e}")
        db.session.rollback()

if __name__ == "__main__":
    with app.app_context():
        seed_data()
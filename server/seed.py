from models import db, User, Token, Alert, Trade, Wallet, Transaction

def seed_data():
    try:
        # Will add some data here
        user1 = User(username='user1', email='user1@example.com')
        db.session.add(user1)

        token1 = Token(name='Bitcoin', symbol='BTC')
        db.session.add(token1)

        alert1 = Alert(user_id=1, token_id=1, price=50000, direction='increase')
        db.session.add(alert1)

        trade1 = Trade(user_id=1, token_id=1, amount=0.01, price=50000, time='2024-01-01 00:00:00', type='buy', status='open', pnl=0, futures=False, order_type='market')  # spot market order to buy 0.01 BTC at $50,000
        db.session.add(trade1)

        trade2 = Trade(user_id=1, token_id=1, amount=0.01, price=60000, time='2024-01-01 00:00:00', type='buy', status='open', pnl=0, futures=True, order_type='limit')  # futures limit order to buy 0.01 BTC at $60,000
        db.session.add(trade2)

        wallet1 = Wallet(user_id=1, balance=100000) 
        db.session.add(wallet1)

        transaction1 = Transaction(wallet_id=1, amount=100000, transaction_type='deposit')  # Initial deposit
        db.session.add(transaction1)

        db.session.commit()
    except Exception as e:
        print(f"An error occurred while seeding data: {e}")

from models import db, User, Token

def seed_data():
    user1 = User(username='user1', email='user1@example.com')
    db.session.add(user1)

    token1 = Token(name='Bitcoin', symbol='BTC')
    db.session.add(token1)

    db.session.commit()

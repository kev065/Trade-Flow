from flask import Flask, jsonify, request, abort
from models import db, ma, User, Token, Alert, Trade, Wallet, Price, Transaction, UserSchema, TokenSchema, AlertSchema, TradeSchema, PriceSchema, WalletSchema, TransactionSchema 
from flask_migrate import Migrate
from services import BinanceService


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)
    ma.init_app(app) 
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return "Trade the Future, Today! Spot the opportunity, Perpetuate the profits!"
    
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        user_schema = UserSchema(many=True)
        return jsonify(user_schema.dump(users)), 200
    
    @app.route('/tokens', methods=['GET'])
    def get_tokens():
        tokens = Token.query.all()
        token_schema = TokenSchema(many=True)
        return jsonify(token_schema.dump(tokens)), 200
    
    @app.route('/alerts', methods=['GET'])
    def get_alerts():
        alerts = Alert.query.all()
        alert_schema = AlertSchema(many=True)
        return jsonify(alert_schema.dump(alerts)), 200
    
    @app.route('/trades', methods=['GET'])
    def get_trades():
        trades = Trade.query.all()
        trade_schema = TradeSchema(many=True)
        return jsonify(trade_schema.dump(trades)), 200
    
    @app.route('/wallets', methods=['GET'])
    def get_wallets():
        wallets = Wallet.query.all()
        wallet_schema = WalletSchema(many=True)
        return jsonify(wallet_schema.dump(wallets)), 200

    @app.route('/transactions', methods=['GET'])
    def get_transactions():
        transactions = Transaction.query.all()
        transaction_schema = TransactionSchema(many=True)
        return jsonify(transaction_schema.dump(transactions)), 200
    
    @app.route('/users/<int:user_id>/watchlist', methods=['GET'])
    def get_user_watchlist(user_id):
        user = User.query.get(user_id)
        if user is None:
            abort(404, description="User not found")
        token_schema = TokenSchema(many=True)
        return jsonify(token_schema.dump(user.watchlist)), 200
    
    @app.route('/prices', methods=['GET'])
    def get_prices():
        prices = Price.query.all()
        price_schema = PriceSchema(many=True)
        return jsonify(price_schema.dump(prices)), 200

    @app.route('/order', methods=['POST'])
    def place_order():
        data = request.get_json()
        if not data:
            abort(400, description="No input data provided")
        required_fields = ['user_id', 'token_id', 'order_type', 'quantity', 'futures']
        if not all(field in data for field in required_fields):
            abort(400, description="Missing required field(s)")
        service = BinanceService()
        price = service.get_price(data['token_id'])  # Get the current price of the token
        trade = Trade(user_id=data['user_id'], token_id=data['token_id'], amount=data['quantity'], price=price, type=data['order_type'], status='open', pnl=0, futures=data['futures'])
        db.session.add(trade)
        db.session.commit()
        trade_schema = TradeSchema()
        return jsonify(trade_schema.dump(trade)), 201

    @app.route('/order/<int:order_id>', methods=['DELETE'])
    def cancel_order(order_id):
        trade = Trade.query.get(order_id)
        if order is None:
            abort(404, description="Trade not found")
        if trade.status != 'open':
            abort(400, description="Cannot cancel a non-open trade")
        trade.status = 'cancelled'
        db.session.commit()
        trade_schema = TradeSchema()
        return jsonify(trade_schema.dump(trade)), 200

    @app.route('/wallet/<int:user_id>', methods=['GET'])
    def get_wallet(user_id):
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if wallet is None:
            abort(404, description="Wallet not found")
        wallet_schema = WalletSchema()
        return jsonify(wallet_schema.dump(wallet)), 200

    @app.route('/transaction', methods=['POST'])
    def make_transaction():
        data = request.get_json()
        if not data:
            abort(400, description="No input data provided")
        required_fields = ['wallet_id', 'amount', 'transaction_type']
        if not all(field in data for field in required_fields):
            abort(400, description="Missing required field(s)")
        transaction = Transaction(wallet_id=data['wallet_id'], amount=data['amount'], transaction_type=data['transaction_type'])
        db.session.add(transaction)
        db.session.commit()
        transaction_schema = TransactionSchema()
        return jsonify(transaction_schema.dump(transaction)), 201

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error=str(e)), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error=str(e)), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()
    app.run(debug=True)



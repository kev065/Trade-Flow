from flask import Flask, jsonify, request, abort
from flask_bcrypt import Bcrypt
from models import db, ma, User, Token, Alert, Trade, Wallet, Price, Transaction, UserSchema, TokenSchema, AlertSchema, TradeSchema, PriceSchema, WalletSchema, TransactionSchema 
from flask_migrate import Migrate
from flask_cors import CORS
from services import BinanceService
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import traceback


bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)
    ma.init_app(app) 
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    app.config['JWT_SECRET_KEY'] = '123456789'
    jwt = JWTManager(app)


    @app.route('/')
    def index():
        return "Trade the Future, Today! Spot the opportunity, Perpetuate the profits!"
    
    @app.route('/users', methods=['GET'])
    def get_all_users():
        users = User.query.all()
        user_schema = UserSchema(many=True)
        return jsonify(user_schema.dump(users)), 200

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        user_schema = UserSchema()
        return jsonify(user_schema.dump(user)), 200
    
    @app.route('/tokens', methods=['GET'])
    def get_all_tokens():
        tokens = Token.query.all()
        token_schema = TokenSchema(many=True)
        return jsonify(token_schema.dump(tokens)), 200

    @app.route('/tokens/<int:token_id>', methods=['GET'])
    def get_token(token_id):
        token = Token.query.get(token_id)
        token_schema = TokenSchema()
        return jsonify(token_schema.dump(token)), 200
    
    @app.route('/alerts', methods=['GET'])
    def get_all_alerts():
        alerts = Alert.query.all()
        alert_schema = AlertSchema(many=True)
        return jsonify(alert_schema.dump(alerts)), 200

    @app.route('/alerts/<int:alert_id>', methods=['GET'])
    def get_alert(alert_id):
        alert = Alert.query.get(alert_id)
        alert_schema = AlertSchema()
        return jsonify(alert_schema.dump(alert)), 200
    
    @app.route('/trades', methods=['GET'])
    def get_all_trades():
        trades = Trade.query.all()
        trade_schema = TradeSchema(many=True)
        return jsonify(trade_schema.dump(trades)), 200

    @app.route('/trades/<int:trade_id>', methods=['GET'])
    def get_trade(trade_id):
        trade = Trade.query.get(trade_id)
        trade_schema = TradeSchema()
        return jsonify(trade_schema.dump(trade)), 200
    
    @app.route('/wallets', methods=['GET'])
    def get_all_wallets():
        wallets = Wallet.query.all()
        wallet_schema = WalletSchema(many=True)
        return jsonify(wallet_schema.dump(wallets)), 200

    @app.route('/wallets/<int:wallet_id>', methods=['GET'])
    def get_single_wallet(wallet_id):
        wallet = Wallet.query.get(wallet_id)
        wallet_schema = WalletSchema()
        return jsonify(wallet_schema.dump(wallet)), 200

    @app.route('/transactions', methods=['GET'])
    def get_all_transactions():
        transactions = Transaction.query.all()
        transaction_schema = TransactionSchema(many=True)
        return jsonify(transaction_schema.dump(transactions)), 200

    @app.route('/transactions/<int:transaction_id>', methods=['GET'])
    def get_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        transaction_schema = TransactionSchema()
        return jsonify(transaction_schema.dump(transaction)), 200
    
    @app.route('/users/<int:user_id>/watchlist', methods=['GET'])
    def get_user_watchlist(user_id):
        user = User.query.get(user_id)
        if user is None:
            abort(404, description="User not found")
        token_schema = TokenSchema(many=True)
        return jsonify(token_schema.dump(user.watchlist)), 200
    
    @app.route('/prices', methods=['GET'])
    def get_all_prices():
        prices = Price.query.all()
        price_schema = PriceSchema(many=True)
        return jsonify(price_schema.dump(prices)), 200

    @app.route('/prices/<int:price_id>', methods=['GET'])
    def get_price(price_id):
        price = Price.query.get(price_id)
        price_schema = PriceSchema()
        return jsonify(price_schema.dump(price)), 200
    

    @app.route('/order', methods=['POST'])
    def place_order():
        try:
            data = request.get_json()
            if not data:
                abort(400, description="No input data provided")
            
            required_fields = ['user_id', 'token_id', 'order_type', 'quantity', 'futures']
            if not all(field in data for field in required_fields):
                abort(400, description="Missing required field(s)")
            
            token_symbol = data['token_id']
            token = Token.query.filter_by(symbol=token_symbol).first()

            if token is None:
                abort(404, description=f"Token with symbol {token_symbol} not found")

            service = BinanceService()
            price = service.get_price(token_symbol)

            order_type = data['order_type'].lower()
            if order_type not in ['buy', 'sell', 'market']:
                abort(400, description=f"Invalid order type: {order_type}")
            
            order_response = service.place_order(token_symbol, order_type, data['quantity'])

            trade = Trade(
                user_id=data['user_id'],
                token_id=token.id,
                amount=data['quantity'],
                price=price,
                type=order_type,
                status='open',
                pnl=0,
                futures=data['futures']
            )

            db.session.add(trade)
            db.session.commit()

            trade_schema = TradeSchema()
            return jsonify(trade_schema.dump(trade)), 201
        except Exception as e:
            traceback.print_exc()
            return jsonify({'error': str(e)}), 400


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

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data:
            abort(400, description="No input data provided")

        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            abort(400, description="Missing required field(s)")

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            abort(400, description="User with this email already exists")

        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()

        access_token = new_user.generate_access_token()

        user_schema = UserSchema()
        return jsonify({"user": user_schema.dump(new_user), "access_token": access_token}), 201
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Invalid request'}), 400
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            user_schema = UserSchema()
            return jsonify(access_token=access_token, user=user_schema.dump(user)), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    
    
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200

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
CORS(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()
    app.run(debug=True)



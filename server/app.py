from flask import Flask, jsonify, request, abort
from models import db, User, Token, Alert, Trade, Wallet, Transaction

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)

    @app.route('/')
    def index():
        return "Trade the Future, Today! Spot the opportunity, Perpetuate the profits!"

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
        return jsonify(message='Order placed successfully'), 201

    @app.route('/order/<int:order_id>', methods=['DELETE'])
    def cancel_order(order_id):
        order = Order.query.get(order_id)
        if order is None:
            abort(404, description="Order not found")
        if order.status != 'open':
            abort(400, description="Cannot cancel a non-open order")
        order.status = 'cancelled'
        db.session.commit()
        return jsonify(message='Order cancelled successfully'), 200

    @app.route('/wallet/<int:user_id>', methods=['GET'])
    def get_wallet(user_id):
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if wallet is None:
            abort(404, description="Wallet not found")
        return jsonify(balance=wallet.balance), 200

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
        return jsonify(message='Transaction made successfully'), 201

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

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()
    app.run(debug=True)


from flask import Flask, jsonify
from models import db, User, Token, Alert, Trade

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)

    @app.route('/')
    def index():
        return "Hello, World!"

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


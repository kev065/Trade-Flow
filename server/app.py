from flask import Flask
from models import db, User, Token, Alert, Trade

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)

    @app.route('/')
    def index():
        return "Hello, World!"

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()
    app.run(debug=True)

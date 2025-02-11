import os
from dotenv import load_dotenv
from flask import Flask
from .extension import db, ma
from .model import User, Product, Order, OrderDetails
from .pages.controller import page
from .auth.controller import auth
from .cart.controller import cart
from .payment.controller import payment

load_dotenv()

def create_db(app):
    with app.app_context():
        if not os.path.exists('library/WebStore.db'):
            db.create_all()
            print('Database created')


def create_app(config_file='config.py'):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config.from_pyfile(config_file)

    db.init_app(app)
    create_db(app)

    ma.init_app(app)

    app.register_blueprint(page)
    app.register_blueprint(auth)
    app.register_blueprint(cart)
    app.register_blueprint(payment)

    return app

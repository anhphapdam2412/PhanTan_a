from datetime import datetime
from .extension import db

# model.py
UserLocal = [
    {'username': '1', 'password': '1'},
    {'username': '2', 'password': '2'},
    {'username': '3', 'password': '3'}
]


class User(db.Model):
    __tablename__ = 'Users'

    username = db.Column(db.String(50), nullable=False, unique=True, primary_key=True,)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('customer', 'admin'), default='customer')
    balance = db.Column(db.Numeric(10, 2), default=100000000)


class Product(db.Model):
    __tablename__ = 'Products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.username', ondelete='CASCADE'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('Pending', 'Processing', 'Shipped', 'Delivered', 'Canceled'), default='Pending')

    user = db.relationship('User', backref=db.backref('orders', cascade='all, delete-orphan'))


class OrderDetails(db.Model):
    __tablename__ = 'OrderDetails'

    order_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', backref=db.backref('order_details', cascade='all, delete-orphan'))
    product = db.relationship('Product', backref=db.backref('order_details', cascade='all, delete-orphan'))

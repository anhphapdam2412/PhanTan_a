from flask import Blueprint
from flask_cors import CORS
from .services import add_to_cart_service, remove_from_cart_service, increase_quantity_service, decrease_quantity_service

cart= Blueprint('cart', __name__)
CORS(cart)

@cart.route('/cart/add', methods=['POST'])
def add_to_cart():
    return add_to_cart_service()
@cart.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    return remove_from_cart_service(product_id)

@cart.route('/cart/increase/<int:product_id>', methods=['POST'])
def increase_quantity(product_id):
    return increase_quantity_service(product_id)

@cart.route('/cart/decrease/<int:product_id>', methods=['POST'])
def decrease_quantity(product_id):
    return decrease_quantity_service(product_id)

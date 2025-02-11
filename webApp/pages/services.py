from flask import render_template
from webApp.cart.services import _get_cart

def render_home_page():
    return render_template('index.html')

def render_contact_page():
    return render_template('contact.html')

def render_introduce_page():
    return render_template('introduce.html')

def render_products_page():
    return render_template('products.html')

def render_payment_page():
    cart = _get_cart()
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    return render_template('payment.html', cart_data=cart, total_price=total_price)


def render_cart_page():
    cart = _get_cart()
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

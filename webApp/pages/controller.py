from flask import Blueprint
from flask_cors import CORS
from .services import (
    render_home_page, render_contact_page, render_introduce_page,
    render_products_page, render_payment_page, render_cart_page
)

page= Blueprint('page', __name__)
CORS(page)

@page.route('/')
@page.route('/index')
def home():
    return render_home_page()

@page.route('/contact')
def contact():
    return render_contact_page()

@page.route('/introduce')
def introduce():
    return render_introduce_page()

@page.route('/products')
def products():
    return render_products_page()

@page.route('/payment')
def payment():
    return render_payment_page()

@page.route('/cart')
def cart_view():
    return render_cart_page()

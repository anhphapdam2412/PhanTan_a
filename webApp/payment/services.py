from flask import Blueprint, request, jsonify, session
import re

VALID_PAYMENT_METHODS = ['cod', 'bank', 'paypal']

def submit_payment_service():
    """Process payment submission."""
    data = request.get_json()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    payment_method = data.get('payment_method', '').strip().lower()
    cart = data.get('cart', [])

    if not name or not phone or not address or not cart:
        return jsonify(success=False, message="Thiếu thông tin cần thiết cho thanh toán."), 400

    if not re.match(r'^\d{9,11}$', phone):
        return jsonify(success=False, message="Số điện thoại không hợp lệ."), 400

    if payment_method not in VALID_PAYMENT_METHODS:
        return jsonify(success=False, message="Phương thức thanh toán không hợp lệ."), 400

    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    total_price_str = f"{total_price:,} VND"

    session['cart'] = []

    return jsonify(success=True, message="Thanh toán thành công!", total_price=total_price_str)

from flask import render_template, abort, request, jsonify, session
from app import app
from app.grpc_client import _authenticate_with_grpc, _get_server_code, _send_user_to_grpc_server, _get_cart, _update_cart
import re
import logging

VALID_PAYMENT_METHODS = ['cod', 'bank', 'paypal']

#=========================== User Management Routes ============================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if _authenticate_with_grpc(username, password):
        session['username'] = username
        return jsonify({"success": True, "login_success": True})
    else:
        return jsonify({"success": False, "login_success": False}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data including cart and username
    return jsonify({"success": True, "message": "Đăng xuất thành công!"})

@app.route('/notify-login-success', methods=['POST'])
def notify_login_success():
    data = request.get_json()
    username = data.get('username')
    if username:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400

@app.route('/session-info')
def session_info():
    username = session.get('username')
    return jsonify({'logged_in': bool(username), 'username': username})

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Thiếu thông tin tài khoản"}), 400

        if not _send_user_to_grpc_server(email, password):
            return jsonify({"message": "Tài khoản đã tồn tại hoặc lỗi đồng bộ với backend"}), 409

        logging.info(f"📥 Người dùng mới: {email}")
        return jsonify({"message": "Đăng ký thành công!"}), 201
    except Exception as e:
        logging.error(f"❌ Lỗi đăng ký: {e}")
        return jsonify({"message": "Đã xảy ra lỗi trong xử lý dữ liệu"}), 500


#=========================== Page Routes ============================
@app.route('/')
@app.route('/index')
def home():
    html_content = _get_server_code()
    if html_content is None:  # If no backend is available
        abort(500, description="Không có backend hoạt động!")
    return render_template('index.html', html=html_content)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/payment')
def payment():
    """Display payment page with cart details."""
    cart = _get_cart()
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    return render_template('payment.html', cart_data=cart, total_price=total_price)

@app.route('/cart')
def cart_view():
    """Display the shopping cart."""
    cart = _get_cart()
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)
#=========================== Cart API ============================

# API endpoints for cart operations
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = int(data.get('id', 0))
    product_name = data.get('name')
    product_price = float(data.get('price', 0))
    image_url = data.get('image_url', '')

    if not product_id or not product_name:
        return jsonify(success=False, message="Dữ liệu sản phẩm không hợp lệ"), 400

    cart = _get_cart()

    for item in cart:
        if 'id' in item and item['id'] == product_id:
            item['quantity'] += 1
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])

    new_item = {
        'id': product_id,
        'name': product_name,
        'price': product_price,
        'quantity': 1,
        'image_url': image_url
    }
    cart.append(new_item)
    _update_cart(cart)
    return jsonify(success=True, new_quantity=1)

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = _get_cart()
    cart = [item for item in cart if item['id'] != product_id]
    _update_cart(cart)
    return jsonify(success=True)

@app.route('/cart/increase/<int:product_id>', methods=['POST'])
def increase_quantity(product_id):
    cart = _get_cart()
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

@app.route('/cart/decrease/<int:product_id>', methods=['POST'])
def decrease_quantity(product_id):
    cart = _get_cart()
    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            else:
                cart.remove(item)
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item.get('quantity', 0))
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

@app.route('/payment/submit', methods=['POST'])
def submit_payment():
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

    logging.info(f"Thanh toán thành công! Tổng tiền: {total_price_str} bằng phương thức {payment_method.upper()}")

    session['cart'] = []

    return jsonify(success=True, message="Thanh toán thành công!", total_price=total_price_str)

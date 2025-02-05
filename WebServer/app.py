from flask import Flask, render_template, request, jsonify, session
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Thay bằng key an toàn của bạn

VALID_PAYMENT_METHODS = {"cod", "bank", "paypal"}  # Các phương thức hợp lệ

def get_cart():
    """Lấy giỏ hàng từ session"""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def update_cart(cart):
    """Cập nhật giỏ hàng trong session"""
    session['cart'] = cart
    session.modified = True

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/products/<int:product_id>')
def product(product_id):
    if 1 <= product_id <= 12:
        return render_template(f'product{product_id}.html')
    else:
        return "Sản phẩm không tồn tại", 404

@app.route('/payment')
def payment():
    """Hiển thị trang thanh toán với giỏ hàng"""
    cart = get_cart()
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    return render_template('payment.html', cart_data=cart, total_price=total_price)

@app.route('/cart')
def cart_view():
    """Hiển thị giỏ hàng"""
    cart = get_cart()
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

# API: Thêm sản phẩm vào giỏ hàng
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = int(data.get('id', 0))
    product_name = data.get('name')
    product_price = float(data.get('price', 0))
    image_url = data.get('image_url', '')

    if not product_id or not product_name:
        return jsonify(success=False, message="Dữ liệu sản phẩm không hợp lệ"), 400

    cart = get_cart()
    
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])

    cart.append({
        'id': product_id,
        'name': product_name,
        'price': product_price,
        'quantity': 1,
        'image_url': image_url
    })
    update_cart(cart)
    return jsonify(success=True, new_quantity=1)

# API: Xóa sản phẩm khỏi giỏ hàng
@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = get_cart()
    cart = [item for item in cart if item['id'] != product_id]
    update_cart(cart)
    return jsonify(success=True)

# API: Tăng số lượng sản phẩm
@app.route('/cart/increase/<int:product_id>', methods=['POST'])
def increase_quantity(product_id):
    cart = get_cart()
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

# API: Giảm số lượng sản phẩm
@app.route('/cart/decrease/<int:product_id>', methods=['POST'])
def decrease_quantity(product_id):
    cart = get_cart()
    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            else:
                cart.remove(item)
            update_cart(cart)
            return jsonify(success=True, new_quantity=item.get('quantity', 0))
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

# API: Thanh toán
@app.route('/payment/submit', methods=['POST'])
def submit_payment():
    """Xử lý thanh toán"""
    data = request.get_json()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    payment_method = data.get('payment_method', '').strip().lower()
    cart = data.get('cart', [])

    # Kiểm tra dữ liệu đầu vào
    if not name or not phone or not address or not cart:
        return jsonify(success=False, message="Thiếu thông tin cần thiết cho thanh toán."), 400

    if not re.match(r'^\d{9,11}$', phone):  # Kiểm tra số điện thoại 9-11 số
        return jsonify(success=False, message="Số điện thoại không hợp lệ."), 400

    if payment_method not in VALID_PAYMENT_METHODS:
        return jsonify(success=False, message="Phương thức thanh toán không hợp lệ."), 400

    # Tính tổng tiền từ giỏ hàng
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    total_price_str = f"{total_price:,} VND"  # Định dạng số tiền

    # Giả lập xử lý thanh toán (thực tế có thể gọi API ngân hàng hoặc PayPal)
    print(f"Thanh toán thành công! Tổng tiền: {total_price_str} bằng phương thức {payment_method.upper()}")

    # Xóa giỏ hàng sau khi thanh toán
    session['cart'] = []

    return jsonify(success=True, message="Thanh toán thành công!", total_price=total_price_str)

if __name__ == '__main__':
    app.run(debug=True)

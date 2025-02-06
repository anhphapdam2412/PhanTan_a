from flask import Flask, render_template, abort, request, jsonify, session
import grpc
import greeter_pb2
import greeter_pb2_grpc
import random
import re

app = Flask(__name__)
 
VALID_PAYMENT_METHODS = {"cod", "bank", "paypal"}  # Các phương thức hợp lệ
GRPC_SERVER_LIST = ['localhost:50051']
app.secret_key = 'your_secret_key_here'  # Thay bằng key an toàn của bạn
current_server = None

# Kết nối với server gRPC để thực hiện xác thực và lấy HTML
def authenticate_with_grpc(username, password):
    global current_server
    
    # Nếu không có server hiện tại, chọn một server ngẫu nhiên để kết nối
    if current_server is None:
        current_server = random.choice(GRPC_SERVER_LIST)
    
    try:
        with grpc.insecure_channel(current_server) as channel:
            stub = greeter_pb2_grpc.GreeterStub(channel)
            response = stub.Authenticate(greeter_pb2.AuthRequest(username=username, password=password), timeout=5)
            if response.success:
                print(f"✅ Đã xác thực thành công với {current_server}")
                return True
    except grpc.RpcError as e:
        print(f"❌ Lỗi kết nối tới {current_server}: {e}")
        current_server = None  # Nếu gặp lỗi, đặt lại và thử lại từ đầu
        return authenticate_with_grpc(username, password)  # Thử lại từ đầu

def get_server_code():
    global current_server
    
    if current_server is None:
        current_server = random.choice(GRPC_SERVER_LIST)  # Chọn một server ngẫu nhiên nếu không có server
    
    try:
        with grpc.insecure_channel(current_server) as channel:
            stub = greeter_pb2_grpc.GreeterStub(channel)
            response = stub.GetIndexPage(greeter_pb2.EmptyRequest(), timeout=5)
            print(f"✅ Đã kết nối với {current_server}")
            return response.html_content
    except grpc.RpcError as e:
        print(f"❌ Lỗi kết nối tới {current_server}: {e}")
        current_server = None  # Nếu gặp lỗi, đặt lại và thử lại từ đầu
        return get_server_code()  # Thử lại từ đầu

def get_cart():
    """Lấy giỏ hàng từ session"""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def update_cart(cart):
    """Cập nhật giỏ hàng trong session"""
    session['cart'] = cart
    session.modified = True

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Xác thực thông qua server gRPC
    if authenticate_with_grpc(username, password):
        return jsonify({"success": True, "login_success": True})
    else:
        return jsonify({"success": False, "login_success": False}), 401

@app.route('/notify-login-success', methods=['POST'])
def notify_login_success():
    data = request.get_json()
    username = data.get('username')
    if username:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400


@app.route('/')
@app.route('/index')
def home():
    html_content = get_server_code()
    if html_content is None:  # Nếu không có backend nào hoạt động
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
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

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

    # Kiểm tra dữ liệu đầu vào hợp lệ
    if not product_id or not product_name:
        return jsonify(success=False, message="Dữ liệu sản phẩm không hợp lệ"), 400

    cart = get_cart()

    # Kiểm tra nếu giỏ hàng trống hoặc không chứa các sản phẩm hợp lệ
    for item in cart:
        # Kiểm tra item có đầy đủ key trước khi so sánh
        if 'id' in item and item['id'] == product_id:
            item['quantity'] += 1
            update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])

    # Thêm sản phẩm mới nếu chưa có trong giỏ hàng
    new_item = {
        'id': product_id,
        'name': product_name,
        'price': product_price,
        'quantity': 1,
        'image_url': image_url
    }
    cart.append(new_item)
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
    app.run(host='0.0.0.0', port=5001, debug=True)

from flask import Flask, render_template, abort, request, jsonify, session
from flask_session import Session
import grpc
import greeter_pb2
import greeter_pb2_grpc
import random
import re

app = Flask(__name__)

VALID_PAYMENT_METHODS = {"cod", "bank", "paypal"}
GRPC_SERVER_LIST = ['localhost:50051', 'localhost:50052', 'localhost:50053']

# Cấu hình session
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
current_server = None

MAX_RETRIES = 3
grpc_channels = {address: grpc.insecure_channel(address) for address in GRPC_SERVER_LIST}


def switch_server():
    """Chuyển sang server gRPC khác khi gặp lỗi."""
    global current_server
    remaining_servers = [srv for srv in GRPC_SERVER_LIST if srv != current_server]
    if remaining_servers:
        current_server = random.choice(remaining_servers)
        print(f"⚠️ Chuyển sang server {current_server}")
    else:
        print("❌ Không có server nào khả dụng!")


def authenticate_with_grpc(username, password):
    global current_server

    if current_server is None:
        current_server = random.choice(GRPC_SERVER_LIST)

    try:
        channel = grpc_channels[current_server]
        stub = greeter_pb2_grpc.GreeterStub(channel)
        response = stub.Authenticate(greeter_pb2.AuthRequest(username=username, password=password), timeout=0.001)
        if response.success:
            print(f"✅ Đã xác thực thành công với {current_server}")
            return True
    except grpc.RpcError as e:
        print(f"❌ Lỗi kết nối tới {current_server}: {e}")
        switch_server()
        return authenticate_with_grpc(username, password) if current_server else False


def get_server_code(retries=0):
    global current_server

    if current_server is None:
        current_server = random.choice(GRPC_SERVER_LIST)

    try:
        with grpc.insecure_channel(current_server) as channel:
            stub = greeter_pb2_grpc.GreeterStub(channel)
            response = stub.GetIndexPage(greeter_pb2.EmptyRequest(), timeout=0.001)
            print(f"✅ Đã kết nối với {current_server}")
            return response.html_content
    except grpc.RpcError as e:
        print(f"❌ Lỗi kết nối tới {current_server}: {e}")
        switch_server()
        if retries < MAX_RETRIES and current_server:
            return get_server_code(retries + 1)
        else:
            return "<h1>500 - Không thể kết nối với backend!</h1>"


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

    if authenticate_with_grpc(username, password):
        session['username'] = username
        return jsonify({"success": True, "login_success": True})
    else:
        return jsonify({"success": False, "login_success": False}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Xóa toàn bộ session bao gồm cả thông tin giỏ hàng và username
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

# Biến lưu trữ thông tin tài khoản trong RAM
users = {}
def send_user_to_grpc_server(email, password):
    global current_server
    try:
        with grpc.insecure_channel(current_server) as channel:
            stub = greeter_pb2_grpc.GreeterStub(channel)
            request = greeter_pb2.SyncRequest(username=email, password=password)
            response = stub.SyncUserData(request)
            if response.success:
                print(f"✅ Đồng bộ tài khoản {email} thành công!")
            else:
                print(f"❌ Đồng bộ tài khoản {email} thất bại!")
    except grpc.RpcError as e:
        print(f"❌ Lỗi khi kết nối đến gRPC Server: {e}")

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Thiếu thông tin tài khoản"}), 400

        if email in users:
            return jsonify({"message": "Email đã được sử dụng!"}), 409

        # Lưu thông tin đăng ký
        users[email] = password
        print(f"📥 Người dùng mới: {email}")

        # Gửi thông tin đến gRPC Server
        send_user_to_grpc_server(email, password)

        return jsonify({"message": "Đăng ký thành công!"}), 201
    except Exception as e:
        return jsonify({"message": "Đã xảy ra lỗi trong xử lý dữ liệu"}), 500



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

    for item in cart:
        if 'id' in item and item['id'] == product_id:
            item['quantity'] += 1
            update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])

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

    if not name or not phone or not address or not cart:
        return jsonify(success=False, message="Thiếu thông tin cần thiết cho thanh toán."), 400

    if not re.match(r'^\d{9,11}$', phone):
        return jsonify(success=False, message="Số điện thoại không hợp lệ."), 400

    if payment_method not in VALID_PAYMENT_METHODS:
        return jsonify(success=False, message="Phương thức thanh toán không hợp lệ."), 400

    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    total_price_str = f"{total_price:,} VND"

    print(f"Thanh toán thành công! Tổng tiền: {total_price_str} bằng phương thức {payment_method.upper()}")

    session['cart'] = []

    return jsonify(success=True, message="Thanh toán thành công!", total_price=total_price_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

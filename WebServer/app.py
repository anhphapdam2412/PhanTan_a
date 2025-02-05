from flask import Flask, render_template, abort, request, jsonify, session
import grpc
import greeter_pb2
import greeter_pb2_grpc
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Thay bằng key an toàn của bạn

GRPC_SERVER_LIST = ['localhost:50051']
current_server = None

def get_grpc_stub():
    global current_server

    if current_server is None:
        current_server = random.choice(GRPC_SERVER_LIST)

    try:
        channel = grpc.insecure_channel(current_server)
        stub = greeter_pb2_grpc.GreeterStub(channel)
        return stub
    except grpc.RpcError as e:
        print(f"❌ Lỗi kết nối tới {current_server}: {e}")
        current_server = None
        return None

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Thiếu thông tin đăng nhập"}), 400

    stub = get_grpc_stub()
    if stub is None:
        return jsonify({"success": False, "message": "Không thể kết nối đến backend"}), 500

    try:
        response = stub.Authenticate(greeter_pb2.AuthRequest(username=username, password=password))
        if response.success:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({"success": True, "login_success": True})
        else:
            return jsonify({"success": False, "login_success": False}), 401
    except grpc.RpcError as e:
        print(f"Lỗi xác thực: {e}")
        return jsonify({"success": False, "message": "Lỗi xác thực"}), 500

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Đã đăng xuất"})

@app.route("/")
@app.route("/index")
def home():
    stub = get_grpc_stub()
    if stub is None:
        abort(500, description="Không có backend hoạt động!")

    try:
        response = stub.GetIndexPage(greeter_pb2.EmptyRequest())
        return render_template('index.html', html_content=response.html_content)
    except grpc.RpcError as e:
        print(f"❌ Lỗi kết nối tới backend: {e}")
        abort(500, description="Không thể kết nối tới backend")

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/products/<int:product_id>')
def product(product_id):
    if 1 <= product_id <= 12:
        return render_template(f'product{product_id}.html')
    else:
        return "Sản phẩm không tồn tại", 404

@app.route('/payment')
def payment():
    cart = session.get('cart', [])
    total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
    return render_template('payment.html', cart_data=cart, total_price=total_price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
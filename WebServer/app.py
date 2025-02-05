from flask import Flask, render_template, abort, request, jsonify
import grpc
import greeter_pb2
import greeter_pb2_grpc
import random

app = Flask(__name__)
 
# Danh sách các server trong mạng Chord (Đây là các server có thể truy cập)
GRPC_SERVER_LIST = ['localhost:50051']
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
def home():
    html_content = get_server_code()
    if html_content is None:  # Nếu không có backend nào hoạt động
        abort(500, description="Không có backend hoạt động!")
    return render_template('index.html', html=html_content)

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
def product_page(product_id):
    if 1 <= product_id <= 12:  # Kiểm tra nếu product_id hợp lệ
        return render_template(f'product{product_id}.html')
    else:
        abort(404, description="Sản phẩm không tồn tại.")
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

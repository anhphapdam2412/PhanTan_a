from flask import Flask, render_template, abort
import grpc
import greeter_pb2
import greeter_pb2_grpc

app = Flask(__name__)

def get_server_code():
    servers = ['localhost:50051', 'localhost:50052']  # Danh sách server ưu tiên
    for server in servers:
        try:
            with grpc.insecure_channel(server) as channel:
                stub = greeter_pb2_grpc.GreeterStub(channel)
                response = stub.GetIndexPage(greeter_pb2.EmptyRequest(), timeout=1)  # Timeout 1 giây
                print(f"✅ Kết nối thành công: {server}")
                return response.html_content
        except grpc.RpcError:
            print(f"❌ Không kết nối được: {server}, thử server khác...")

    return None  # Không có server nào hoạt động

@app.route('/')
def home():
    html_content = get_server_code()
    
    if html_content is None:  # Nếu không có backend, báo lỗi 500
        abort(500, description="Không có backend hoạt động!")

    return render_template('index.html', html=html_content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

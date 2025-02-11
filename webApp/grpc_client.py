import grpc
from grpc_services import greeter_pb2, greeter_pb2_grpc
import random

SERVER_LIST = ['localhost:50051', 'localhost:50052']
current_server = None

def change_server():
    """Chọn server mới từ danh sách còn lại."""
    global current_server
    available_servers = [server for server in SERVER_LIST if server != current_server]
    if not available_servers:
        raise Exception("Không có server nào khả dụng.")
    current_server = random.choice(available_servers)
    print(f"Chuyển sang server mới: {current_server}")
    return current_server

def connect_with_fallback(func):
    """Kết nối gRPC với xử lý fallback khi server gặp lỗi."""
    def wrapper(*args, **kwargs):
        global current_server
        attempts = 0

        while attempts < len(SERVER_LIST):
            if current_server is None:
                current_server = change_server()

            try:
                print(f"Đang kết nối đến server: {current_server}")
                with grpc.insecure_channel(current_server) as channel:
                    stub = greeter_pb2_grpc.GreeterStub(channel)
                    return func(stub, *args, **kwargs)

            except grpc.RpcError as e:
                print(f"Lỗi gRPC trên server {current_server}: {e.details()}")
                current_server = None  # Hủy server hiện tại
                attempts += 1  # Tăng số lần thử

        return "Không thể kết nối với bất kỳ server nào"
    return wrapper

@connect_with_fallback
def login(stub, username, password):
    response = stub.Authenticate(greeter_pb2.UserRequest(username=username, password=password))
    if response.success:
        return "Success"
    return f"Failed: Lỗi khi đăng nhập"

@connect_with_fallback
def register(stub, username, password):
    response = stub.Register(greeter_pb2.UserRequest(username=username, password=password))
    if response.success:
        return "Success"
    return f"Failed: Lỗi khi đăng ký {response.status}"

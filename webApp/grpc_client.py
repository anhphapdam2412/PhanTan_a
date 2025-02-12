import grpc
import threading
import time
import random
from grpc_services import greeter_pb2, greeter_pb2_grpc

# ✅ Danh sách các gRPC servers
GRPC_SERVERS = ["127.0.0.1:50051", "127.0.0.1:50052", "127.0.0.1:50053"]
ACTIVE_SERVERS = []  # Danh sách server đang hoạt động

def check_server(server):
    """Kiểm tra xem server có đang hoạt động không bằng heartbeat (ping)."""
    try:
        channel = grpc.insecure_channel(server)
        grpc.channel_ready_future(channel).result(timeout=1)  # Kiểm tra trong 1 giây
        return True
    except grpc.FutureTimeoutError:
        return False

def update_active_servers():
    """Cập nhật danh sách server đang hoạt động mỗi 10 giây."""
    global ACTIVE_SERVERS
    while True:
        active_list = [s for s in GRPC_SERVERS if check_server(s)]
        ACTIVE_SERVERS = active_list
        print(f"🔄 Cập nhật server hoạt động: {ACTIVE_SERVERS}")
        time.sleep(10)  # Cập nhật mỗi 10 giây

# ✅ Chạy heartbeat trong background
heartbeat_thread = threading.Thread(target=update_active_servers, daemon=True)
heartbeat_thread.start()

def get_stub():
    """Chọn một server đang hoạt động và tạo stub gRPC"""
    if not ACTIVE_SERVERS:
        raise Exception("❌ Không có server nào khả dụng!")

    server = random.choice(ACTIVE_SERVERS)  # Chọn server ngẫu nhiên
    print(f"✅ Kết nối đến: {server}")
    channel = grpc.insecure_channel(server)
    return greeter_pb2_grpc.GreeterStub(channel)

def login(username, password):
    """Gửi request login đến gRPC server đã chọn."""
    try:
        stub = get_stub()
        response = stub.Authenticate(greeter_pb2.UserRequest(username=username, password=password))
        return "Success" if response.success else f"Failed: {response.message}"
    except grpc.RpcError as e:
        return f"gRPC Error: {e.code()} - {e.details()}"

def register(username, password):
    """Gửi request register đến gRPC server đã chọn."""
    try:
        stub = get_stub()
        response = stub.Register(greeter_pb2.UserRequest(username=username, password=password))
        return "Success" if response.success else f"Failed: {response.message}"
    except grpc.RpcError as e:
        return f"gRPC Error: {e.code()} - {e.details()}"

def delete(username):
    """Gửi request xóa user đến gRPC server đã chọn."""
    try:
        stub = get_stub()
        response = stub.DeleteUser(greeter_pb2.UserRequest(username=username))
        return "Success" if response.success else f"Failed: {response.message}"
    except grpc.RpcError as e:
        return f"gRPC Error: {e.code()} - {e.details()}"

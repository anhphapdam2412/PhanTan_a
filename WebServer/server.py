import grpc
from concurrent import futures
import greeter_pb2
import greeter_pb2_grpc
import threading
# Biến lưu trữ tài khoản trong RAM
user_db = {'a@gmail.com':'1'}


class GreeterService(greeter_pb2_grpc.GreeterServicer):
    def Authenticate(self, request, context):
        username = request.username
        password = request.password

        if username in user_db and user_db[username] == password:
            print(f"✅ Xác thực thành công cho {username}")
            return greeter_pb2.AuthResponse(success=True)

        print(f"❌ Xác thực thất bại cho {username}")
        return greeter_pb2.AuthResponse(success=False)

    def SyncUserData(self, request, context):
        """Đồng bộ tài khoản từ server khác"""
        username = request.username
        password = request.password
        user_db[username] = password
        print(f"📥 Đồng bộ tài khoản {username} từ server khác")
        return greeter_pb2.SyncResponse(success=True)

def sync_with_other_server(username, password, target_server):
    """Gửi yêu cầu đồng bộ tài khoản đến server khác"""
    try:
        with grpc.insecure_channel(target_server) as channel:
            stub = greeter_pb2_grpc.GreeterStub(channel)
            request = greeter_pb2.SyncRequest(username=username, password=password)
            response = stub.SyncUserData(request, timeout=5)
            if response.success:
                print(f"✅ Đồng bộ tài khoản {username} sang {target_server} thành công")
    except grpc.RpcError as e:
        print(f"❌ Lỗi đồng bộ với {target_server}: {e}")
def periodic_sync(other_server):
    """Thực hiện đồng bộ định kỳ với server khác."""
    for username, password in user_db.items():
        sync_with_other_server(username, password, other_server)
    # Lên lịch cho lần đồng bộ tiếp theo sau 10 giây
    threading.Timer(10, periodic_sync, [other_server]).start()
    
def serve(port, other_server):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    server.add_insecure_port(f'[::]:{port}')
    print(f"gRPC Server đang chạy trên cổng {port}...")
    server.start()

    # Kích hoạt đồng bộ định kỳ sau khi server khởi động
    periodic_sync(other_server)

    server.wait_for_termination()


if __name__ == "__main__":
    import sys

    # Cài đặt giá trị mặc định cho server
    servers = {
        "50051": "localhost:50052",
        "50052": "localhost:50051"
    }

    port = '50051'
    
    if port not in servers:
        print("❌ Cổng không hợp lệ. Vui lòng chọn 50051 hoặc 50052.")
        sys.exit(1)

    other_server = servers[port]
    print(port,other_server)
    serve(int(port), other_server)

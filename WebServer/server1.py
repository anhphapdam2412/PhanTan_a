import grpc
from concurrent import futures
import greeter_pb2
import greeter_pb2_grpc
import threading
import sys
import time

# Biến lưu trữ tài khoản trong RAM
user_db = {'1@gmail.com': '1'}
db_lock = threading.Lock()

# Danh sách server và cổng
server_ports = [50051, 50052, 50053]

class GreeterService(greeter_pb2_grpc.GreeterServicer):
    def GetIndexPage(self, request, context):
        return greeter_pb2.IndexResponse(html_content="<h1>Welcome to the Home Page</h1>")

    def Authenticate(self, request, context):
        username = request.username
        password = request.password

        with db_lock:
            if username in user_db and user_db[username] == password:
                print(f"✅ Xác thực thành công cho {username}")
                return greeter_pb2.AuthResponse(success=True)

        print(f"❌ Xác thực thất bại cho {username}")
        return greeter_pb2.AuthResponse(success=False)

    def SyncUserData(self, request, context):
        username = request.username
        password = request.password

        with db_lock:
            user_db[username] = password
            print(f"📥 Đồng bộ tài khoản {username} từ server khác")

        return greeter_pb2.SyncResponse(success=True)


def build_finger_table(port):
    index = server_ports.index(port)
    finger_table = [(index + 2 ** i) % len(server_ports) for i in range(len(server_ports))]
    finger_table = [server_ports[i] for i in finger_table]

    print(f"📝 Finger Table cho cổng {port}: {finger_table}")
    return finger_table


def sync_with_finger_table(username, password, finger_table):
    for target_port in finger_table:
        target_server = f"localhost:{target_port}"
        try:
            with grpc.insecure_channel(target_server) as channel:
                grpc.channel_ready_future(channel).result(timeout=0.001)
                stub = greeter_pb2_grpc.GreeterStub(channel)
                request = greeter_pb2.SyncRequest(username=username, password=password)
                response = stub.SyncUserData(request, timeout=0.001)
                if response.success:
                    print(f"✅ Đồng bộ tài khoản {username} sang {target_server} thành công")
        except grpc.FutureTimeoutError:
            print(f"❌ Không thể kết nối tới {target_server} (Timeout)")
        except grpc.RpcError as e:
            print(f"❌ Lỗi đồng bộ với {target_server}: {e}")


def periodic_sync(finger_table):
    print("🔄 Bắt đầu đồng bộ định kỳ...")
    with db_lock:
        for username, password in user_db.items():
            sync_with_finger_table(username, password, finger_table)
    threading.Timer(60, periodic_sync, [finger_table]).start()


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    server.add_insecure_port(f'[::]:{port}')
    print(f"gRPC Server đang chạy trên cổng {port}...")

    finger_table = build_finger_table(port)

    periodic_sync(finger_table)

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50051
    if port not in server_ports:
        print("❌ Cổng không hợp lệ. Vui lòng chọn từ 50051 đến 50053.")
        sys.exit(1)
    serve(port)

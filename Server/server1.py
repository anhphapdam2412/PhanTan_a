import grpc
from concurrent import futures
import greeter_pb2
import greeter_pb2_grpc
import threading
import sys
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# In-memory user storage (for demonstration purposes only)
user_db = {'1@gmail.com': '1'}
db_lock = threading.Lock()

# List of server ports
server_ports = [50051, 50052, 50053]

class GreeterService(greeter_pb2_grpc.GreeterServicer):
    def GetIndexPage(self, request, context):
        return greeter_pb2.IndexResponse(html_content="<h1>Welcome to the Home Page</h1>")

    def Authenticate(self, request, context):
        username, password = request.username, request.password
        with db_lock:
            success = username in user_db and user_db[username] == password
        print(f"✅ Xác thực thành công cho {username}" if success else f"❌ Xác thực thất bại cho {username}")
        return greeter_pb2.AuthResponse(success=success)

    def SyncUserData(self, request, context):
        username, password = request.username, request.password
        with db_lock:
            user_db[username] = password
        print(f"📥 Đồng bộ tài khoản {username} từ server khác")
        return greeter_pb2.SyncResponse(success=True)
    
    def Register(self, request, context):
        username, password = request.username, request.password
        logging.info(f"📥 Nhận yêu cầu đăng ký từ {username}")

        # Kiểm tra tài khoản có trong DB cục bộ
        with db_lock:
            if username in user_db:
                logging.warning(f"⚠️ Tài khoản {username} đã tồn tại trong server cục bộ.")
                return greeter_pb2.AuthResponse(success=False, message="Tài khoản đã tồn tại.")

        # Kiểm tra tài khoản có trong các server khác
        for target_port in server_ports:
            if target_port == int(sys.argv[1]):  # Bỏ qua chính server hiện tại
                continue
            try:
                with grpc.insecure_channel(f'localhost:{target_port}') as channel:
                    stub = greeter_pb2_grpc.GreeterStub(channel)
                    check_request = greeter_pb2.CheckUserExistenceRequest(username=username)
                    response = stub.CheckUserExistence(check_request)
                    if response.exists:
                        logging.warning(f"⚠️ Tài khoản {username} đã tồn tại trên server khác tại cổng {target_port}")
                        return greeter_pb2.AuthResponse(success=False, message="Tài khoản đã tồn tại trên server khác.")
            except grpc.RpcError as e:
                logging.error(f"❌ Lỗi khi kiểm tra server {target_port}: {e.details()}")

        # Đăng ký vào DB cục bộ
        with db_lock:
            user_db[username] = password
            logging.info(f"✅ Đăng ký thành công tài khoản {username} trong server cục bộ.")

        # Đồng bộ với các server trong Finger Table
        sync_with_finger_table(username, password, build_finger_table(int(sys.argv[1])))

        logging.info(f"✅ Hoàn thành đăng ký và đồng bộ tài khoản {username}")
        return greeter_pb2.AuthResponse(success=True, message="Đăng ký thành công.")


    def CheckUserExistence(self, request, context):
        with db_lock:
            exists = request.username in user_db
        return greeter_pb2.CheckUserExistenceResponse(exists=exists)

def build_finger_table(port):
    index = server_ports.index(port)
    finger_table = [server_ports[(index + 2 ** i) % len(server_ports)] for i in range(len(server_ports))]
    print(f"📝 Finger Table cho cổng {port}: {finger_table}")
    return finger_table

def sync_with_finger_table(username, password, finger_table):
    for target_port in finger_table:
        target_server = f"localhost:{target_port}"
        try:
            with grpc.insecure_channel(target_server) as channel:
                grpc.channel_ready_future(channel).result(timeout=3)
                stub = greeter_pb2_grpc.GreeterStub(channel)
                request = greeter_pb2.SyncRequest(username=username, password=password)
                if stub.SyncUserData(request, timeout=3).success:
                    print(f"✅ Đồng bộ tài khoản {username} sang {target_server} thành công")
        except grpc.FutureTimeoutError:
            logging.warning(f"⚠️ Không thể kết nối tới {target_server} (Timeout)")
        except grpc.RpcError as e:
            logging.error(f"❌ Lỗi đồng bộ với {target_server}: {e.details()}")
            if "Connect" in str(e) and "refused" in str(e):
                logging.warning(f"⚠️ Bỏ qua server {target_server} vì không thể kết nối")

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

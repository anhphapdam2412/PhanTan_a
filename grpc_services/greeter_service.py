import grpc
import json
import threading
import time
from grpc_services import greeter_pb2_grpc, greeter_pb2
from webApp import model, config
from webApp.model import UserLocal
import sys
from concurrent import futures

SECRET_KEY = config.SECRET_KEY
SERVER_PORTS = [50051, 50052, 50053]
BACKUP_FILE_PATH = 'user_data_backup.json'

def portIsValid():
    """Kiểm tra và trả về cổng hợp lệ từ đối số dòng lệnh."""
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50051
    if port not in SERVER_PORTS:
        print("❌ Cổng không hợp lệ. Vui lòng chọn từ 50051 đến 50053.")
        sys.exit(1)
    return port

class GreeterService(greeter_pb2_grpc.GreeterServicer):
    
    def _send_registration_to_server(self, server, username, password):
        """Gửi thông tin đăng ký đến một server cụ thể."""
        try:
            print(f"Gửi thông tin đăng ký tới server: {server}")
            with grpc.insecure_channel(f'localhost:{server}') as channel:
                stub = greeter_pb2_grpc.GreeterStub(channel)
                response = stub.Register(greeter_pb2.UserRequest(username=username, password=password, status="existing"))
                if response.success:
                    print(f"Đã gửi thông tin đăng ký thành công đến {server}")
                else:
                    print(f"Không thể gửi thông tin đăng ký đến {server}: {response.message}")
        except grpc.RpcError as e:
            print(f"Lỗi khi gửi thông tin đến server {server}: {e.details()}")


    def _backup_data(self):
        """Lưu dữ liệu người dùng vào file JSON."""
        with open(BACKUP_FILE_PATH, 'w') as f:
            json.dump(UserLocal, f, indent=4)
        print(f"Dữ liệu đã được sao lưu vào {BACKUP_FILE_PATH}")
    
    def _schedule_backup(self):
        """Chạy sao lưu định kỳ mỗi 60 giây."""
        while True:
            time.sleep(60)  # Chờ 60 giây
            self._backup_data()  # Thực hiện sao lưu

    def _broadcast_registration(self, username, password):
        """Gửi thông tin đăng ký đến tất cả server khác, tránh gửi đến chính mình."""
        port = portIsValid()

        for server in SERVER_PORTS:
            if server == port:
                continue
            # Tạo và bắt đầu một luồng mới cho mỗi server
            thread = threading.Thread(target=self._send_registration_to_server, args=(server, username, password))
            thread.daemon = True  # Đảm bảo luồng sẽ tự động kết thúc khi ứng dụng tắt
            thread.start()  # Bắt đầu luồng

    def Authenticate(self, request, context):
        username = request.username
        password = request.password

        # Kiểm tra thông tin đăng nhập trong danh sách UserLocal
        for user in UserLocal:
            if user['username'] == username and user['password'] == password:
                print(f"Đăng nhập thành công: {username}")
                return greeter_pb2.AuthResponse(success=True)
        return greeter_pb2.AuthResponse(status="Failure", success=False)

    def Register(self, request, context):
        username = request.username
        password = request.password

        # Kiểm tra xem người dùng đã tồn tại chưa
        for user in UserLocal:
            if user['username'] == username:
                return greeter_pb2.RegisterResponse(success=False, message="Tài khoản đã tồn tại.", status="Exist")
        
        # Thêm người dùng vào danh sách UserLocal
        print(f"Đăng ký tài khoản mới: {username}")
        UserLocal.append({'username': username, 'password': password})
        
        self._broadcast_registration(username, password)
        
        # Lưu dữ liệu vào file sau khi có người dùng mới
        self._backup_data()
        
        return greeter_pb2.RegisterResponse(success=True, message="Đăng ký thành công.")

    def _broadcast_periodically(self):
        """Chạy định kỳ để gửi thông tin đăng ký mới đến các server khác mỗi 60 giây."""
        while True:
            time.sleep(60)  # Chờ 60 giây trước khi gửi lại thông tin đăng ký
            for user in UserLocal:
                # Gửi thông tin người dùng đến các server khác
                self._broadcast_registration(user['username'], user['password'])

# Khởi tạo và bắt đầu chạy sao lưu và gửi thông tin định kỳ
def start_services():
    greeter_service = GreeterService()

    # Tạo một luồng mới để chạy sao lưu định kỳ
    backup_thread = threading.Thread(target=greeter_service._schedule_backup)
    backup_thread.daemon = True  # Đảm bảo luồng này sẽ kết thúc khi ứng dụng tắt
    backup_thread.start()

    # Tạo một luồng mới để gửi thông tin đăng ký mỗi 60 giây
    broadcast_thread = threading.Thread(target=greeter_service._broadcast_periodically)
    broadcast_thread.daemon = True  # Đảm bảo luồng này sẽ kết thúc khi ứng dụng tắt
    broadcast_thread.start()

    # Khởi tạo server và gắn cổng hợp lệ
    port = portIsValid()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(greeter_service, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()

# Gọi hàm bắt đầu sao lưu và gửi thông tin đăng ký định kỳ ngay khi ứng dụng khởi chạy
start_services()

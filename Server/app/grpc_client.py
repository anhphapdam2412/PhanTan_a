import grpc
import greeter_pb2
import greeter_pb2_grpc
import random
import logging
from flask import session

# Constants
GRPC_SERVER_LIST = ['localhost:50051', 'localhost:50052', 'localhost:50053']
MAX_RETRIES = 3

# gRPC channels initialization
grpc_channels = {address: grpc.insecure_channel(address) for address in GRPC_SERVER_LIST}
current_server = None


def _connect_to_grpc(func):
    def wrapper(*args, **kwargs):
        global current_server
        if current_server is None:
            _select_initial_server()

        for attempt in range(MAX_RETRIES):
            if not current_server:
                logging.error("❌ Không có server nào khả dụng!")
                break

            try:
                channel = grpc_channels[current_server]
                logging.info(f"🔗 Đang kết nối tới server {current_server} (Lần {attempt + 1})")
                return func(channel, *args, **kwargs)
            except grpc.RpcError as e:
                logging.error(f"❌ Lỗi kết nối tới {current_server}: {e.details()}")
                _switch_server()
            except Exception as e:
                logging.error(f"❌ Lỗi không xác định: {e}")
                break

        logging.error("❌ Không thể kết nối tới bất kỳ backend nào sau nhiều lần thử!")
        return None
    return wrapper


def _select_initial_server():
    """Chọn server ban đầu và loại bỏ các server không khả dụng."""
    global current_server
    available_servers = []

    for server in GRPC_SERVER_LIST:
        if test_grpc_connection(server):
            available_servers.append(server)

    if available_servers:
        current_server = random.choice(available_servers)
        logging.info(f"✅ Server khởi động ban đầu: {current_server}")
    else:
        logging.error("❌ Không có server nào khả dụng ban đầu!")
        current_server = None


def _switch_server():
    """Chuyển sang server khác khi có lỗi kết nối."""
    global current_server
    remaining_servers = [srv for srv in GRPC_SERVER_LIST if srv != current_server]

    if remaining_servers:
        current_server = random.choice(remaining_servers)
        logging.warning(f"⚠️ Chuyển sang server {current_server}")
    else:
        logging.error("❌ Không có server nào khả dụng!")
        current_server = None


def test_grpc_connection(server_address):
    """Kiểm tra kết nối gRPC đơn giản."""
    try:
        with grpc.insecure_channel(server_address) as channel:
            grpc.channel_ready_future(channel).result(timeout=3)
            logging.info(f"✅ Kết nối thành công tới {server_address}")
            return True
    except grpc.FutureTimeoutError:
        logging.error(f"❌ Không thể kết nối tới {server_address} (Timeout)")
    except grpc.RpcError as e:
        logging.error(f"❌ Lỗi gRPC tới {server_address}: {e.details()}")
    return False


#==============================================================================

def _get_cart():
    """Retrieve cart from session."""
    return session.setdefault('cart', [])


def _update_cart(cart):
    """Update cart in session."""
    session['cart'] = cart
    session.modified = True


#==============================================================================

@_connect_to_grpc
def _send_user_to_grpc_server(channel, email, password):
    try:
        stub = greeter_pb2_grpc.GreeterStub(channel)

        # Kiểm tra nếu user đã tồn tại
        check_request = greeter_pb2.AuthRequest(username=email, password=password)
        existence_response = stub.CheckUserExistence(check_request)

        if existence_response.exists:
            logging.warning(f"⚠️ Tài khoản {email} đã tồn tại trên server.")
            return False

        # Nếu chưa tồn tại, thực hiện đăng ký
        request = greeter_pb2.RegisterRequest(username=email, password=password)
        response = stub.Register(request)

        if response.success:
            logging.info(f"✅ Đăng ký tài khoản {email} thành công trên server.")
            return True
        else:
            logging.warning(f"⚠️ {response.message}")

    except grpc.FutureTimeoutError:
        logging.error("❌ Không thể kết nối tới server (Timeout)")
    except grpc.RpcError as e:
        logging.error(f"❌ Lỗi khi gửi request GRPC: {e.details()}")

    return False


@_connect_to_grpc
def _check_user_existence(channel, email):
    stub = greeter_pb2_grpc.GreeterStub(channel)
    request = greeter_pb2.AuthRequest(username=email)
    response = stub.CheckUserExistence(request)
    return response.exists


@_connect_to_grpc
def _authenticate_with_grpc(channel, username, password):
    stub = greeter_pb2_grpc.GreeterStub(channel)
    response = stub.Authenticate(greeter_pb2.AuthRequest(username=username, password=password), timeout=3)
    if response.success:
        logging.info(f"✅ Đã xác thực thành công với {current_server}")
        return True
    else:
        return False

@_connect_to_grpc
def _get_server_code(channel):
    stub = greeter_pb2_grpc.GreeterStub(channel)
    response = stub.GetIndexPage(greeter_pb2.EmptyRequest(), timeout=3)
    logging.info(f"✅ Đã kết nối với {current_server}")
    return response.html_content

#==============================================================================

# Kiểm tra kết nối server ban đầu
for port in [50051, 50052, 50053]:
    test_grpc_connection(f'localhost:{port}')

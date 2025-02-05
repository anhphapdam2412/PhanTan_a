import grpc
from concurrent.futures import ThreadPoolExecutor
import greeter_pb2
import greeter_pb2_grpc
import random
import json
import re
from datetime import datetime

USER_DATA = {"a@gmail.com": "1"}

# Lưu giỏ hàng của mỗi user vào bộ nhớ đơn giản cho demo (production nên dùng DB)
CART_DATA = {}

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    def GetIndexPage(self, request, context):
        try:
            with open("index.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            return greeter_pb2.HtmlResponse(html_content=html_content)
        except FileNotFoundError:
            return greeter_pb2.HtmlResponse(html_content="<h1>404 - File Not Found</h1>")

    def Authenticate(self, request, context):
        username = request.username
        password = request.password

        if username in USER_DATA and USER_DATA[username] == password:
            print(f"{datetime.now()} - Đăng nhập thành công: {username}")
            return greeter_pb2.AuthResponse(success=True)
        else:
            print(f"{datetime.now()} - Đăng nhập thất bại: {username}")
            return greeter_pb2.AuthResponse(success=False)

    def GetCart(self, request, context):
        username = request.username
        cart = CART_DATA.get(username, [])
        cart_json = json.dumps(cart)
        return greeter_pb2.CartResponse(cart_data=cart_json)

    def AddToCart(self, request, context):
        username = request.username
        product = json.loads(request.product_data)

        if username not in CART_DATA:
            CART_DATA[username] = []

        # Kiểm tra sản phẩm có tồn tại trong giỏ hàng không
        for item in CART_DATA[username]:
            if item['id'] == product['id']:
                item['quantity'] += 1
                return greeter_pb2.CartUpdateResponse(success=True)

        CART_DATA[username].append(product)
        return greeter_pb2.CartUpdateResponse(success=True)

    def SubmitPayment(self, request, context):
        username = request.username
        data = json.loads(request.payment_data)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        address = data.get('address', '').strip()
        payment_method = data.get('payment_method', '').strip().lower()
        cart = CART_DATA.get(username, [])

        if not name or not phone or not address or not cart:
            return greeter_pb2.PaymentResponse(success=False, message="Thiếu thông tin cần thiết cho thanh toán.")

        if not re.match(r'^\d{9,11}$', phone):
            return greeter_pb2.PaymentResponse(success=False, message="Số điện thoại không hợp lệ.")

        if payment_method not in {"cod", "bank", "paypal"}:
            return greeter_pb2.PaymentResponse(success=False, message="Phương thức thanh toán không hợp lệ.")

        total_price = sum(item['quantity'] * item.get('price', 0) for item in cart)
        total_price_str = f"{total_price:,} VND"

        # Xóa giỏ hàng sau khi thanh toán
        CART_DATA[username] = []
        print(f"Thanh toán thành công cho {username}. Tổng tiền: {total_price_str}")

        return greeter_pb2.PaymentResponse(success=True, message="Thanh toán thành công!", total_price=total_price_str)


def serve_grpc():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve_grpc()
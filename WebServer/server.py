import grpc
from concurrent.futures import ThreadPoolExecutor
import greeter_pb2
import greeter_pb2_grpc
import random

USER_DATA = {"a@gmail.com": "1"}


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
            return greeter_pb2.AuthResponse(success=True)
        else:
            return greeter_pb2.AuthResponse(success=False)

    def NotifyLoginSuccess(self, request, context):
        username = request.username
        print(f"Thông báo: Người dùng {username} đã đăng nhập thành công.")
        return greeter_pb2.LoginSuccessResponse(success=True)
        

def serve_grpc():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve_grpc()

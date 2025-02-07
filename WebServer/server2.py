import grpc
from concurrent.futures import ThreadPoolExecutor
import greeter_pb2
import greeter_pb2_grpc
import random
import json
import re
from datetime import datetime

USER_DATA = {"b@gmail.com": "1"}
INDEX_FILE_PATH = "WebServer/templates/index.html"

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):

    def GetIndexPage(self, request, context):
        try:
            with open(INDEX_FILE_PATH, "r", encoding="utf-8") as f:
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


def serve_grpc():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("gRPC Server is running on port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve_grpc()
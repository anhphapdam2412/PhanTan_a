import sys
import grpc
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import greeter_pb2
import greeter_pb2_grpc

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    def GetIndexPage(self, request, context):
        try:
            with open(__file__, "r", encoding="utf-8") as f:
                html_content = f.read()
            return greeter_pb2.HtmlResponse(html_content=html_content)
        except FileNotFoundError:
            return greeter_pb2.HtmlResponse(html_content="<h1>404 - File Not Found</h1>")

def serve_grpc():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("gRPC Server is running on port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve_grpc()

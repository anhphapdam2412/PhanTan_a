import grpc
from grpc_services import greeter_pb2_grpc, greeter_service
from concurrent import futures
from grpc_services.greeter_service import portIsValid

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(greeter_service.GreeterService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"gRPC server đang chạy trên cổng {port}...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve(portIsValid)

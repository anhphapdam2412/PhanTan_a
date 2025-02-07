# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import greeter_pb2 as greeter__pb2

GRPC_GENERATED_VERSION = '1.69.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in greeter_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class GreeterStub(object):
    """Dịch vụ Greeter cho gRPC
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Authenticate = channel.unary_unary(
                '/greeter.Greeter/Authenticate',
                request_serializer=greeter__pb2.AuthRequest.SerializeToString,
                response_deserializer=greeter__pb2.AuthResponse.FromString,
                _registered_method=True)
        self.GetIndexPage = channel.unary_unary(
                '/greeter.Greeter/GetIndexPage',
                request_serializer=greeter__pb2.EmptyRequest.SerializeToString,
                response_deserializer=greeter__pb2.IndexResponse.FromString,
                _registered_method=True)
        self.SyncUserData = channel.unary_unary(
                '/greeter.Greeter/SyncUserData',
                request_serializer=greeter__pb2.SyncRequest.SerializeToString,
                response_deserializer=greeter__pb2.SyncResponse.FromString,
                _registered_method=True)


class GreeterServicer(object):
    """Dịch vụ Greeter cho gRPC
    """

    def Authenticate(self, request, context):
        """Xác thực người dùng
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIndexPage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SyncUserData(self, request, context):
        """Đồng bộ tài khoản giữa các server
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GreeterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Authenticate': grpc.unary_unary_rpc_method_handler(
                    servicer.Authenticate,
                    request_deserializer=greeter__pb2.AuthRequest.FromString,
                    response_serializer=greeter__pb2.AuthResponse.SerializeToString,
            ),
            'GetIndexPage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIndexPage,
                    request_deserializer=greeter__pb2.EmptyRequest.FromString,
                    response_serializer=greeter__pb2.IndexResponse.SerializeToString,
            ),
            'SyncUserData': grpc.unary_unary_rpc_method_handler(
                    servicer.SyncUserData,
                    request_deserializer=greeter__pb2.SyncRequest.FromString,
                    response_serializer=greeter__pb2.SyncResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'greeter.Greeter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('greeter.Greeter', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Greeter(object):
    """Dịch vụ Greeter cho gRPC
    """

    @staticmethod
    def Authenticate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/greeter.Greeter/Authenticate',
            greeter__pb2.AuthRequest.SerializeToString,
            greeter__pb2.AuthResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetIndexPage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/greeter.Greeter/GetIndexPage',
            greeter__pb2.EmptyRequest.SerializeToString,
            greeter__pb2.IndexResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SyncUserData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/greeter.Greeter/SyncUserData',
            greeter__pb2.SyncRequest.SerializeToString,
            greeter__pb2.SyncResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from prime_proto.prime_finder_core import get_largest_prime_pb2 as prime__proto_dot_prime__finder__core_dot_get__largest__prime__pb2


class LargestPrimeFinderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetLargestPrime = channel.unary_unary(
                '/prime_finder_core.get_largest_prime.LargestPrimeFinder/GetLargestPrime',
                request_serializer=prime__proto_dot_prime__finder__core_dot_get__largest__prime__pb2.InputRequest.SerializeToString,
                response_deserializer=prime__proto_dot_prime__finder__core_dot_get__largest__prime__pb2.UnsignedIntegerResponse.FromString,
                )


class LargestPrimeFinderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetLargestPrime(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LargestPrimeFinderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetLargestPrime': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLargestPrime,
                    request_deserializer=prime__proto_dot_prime__finder__core_dot_get__largest__prime__pb2.InputRequest.FromString,
                    response_serializer=prime__proto_dot_prime__finder__core_dot_get__largest__prime__pb2.UnsignedIntegerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'prime_finder_core.get_largest_prime.LargestPrimeFinder', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LargestPrimeFinder(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetLargestPrime(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prime_finder_core.get_largest_prime.LargestPrimeFinder/GetLargestPrime',
            prime__proto_dot_prime__finder__core_dot_get__largest__prime__pb2.InputRequest.SerializeToString,
            prime__proto_dot_prime__finder__core_dot_get__largest__prime__pb2.UnsignedIntegerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

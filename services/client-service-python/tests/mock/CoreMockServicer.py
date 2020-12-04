from prime_proto.prime_finder_core import get_largest_prime_pb2
from prime_proto.prime_finder_core import get_largest_prime_pb2_grpc


class CoreMockServicer(get_largest_prime_pb2_grpc.LargestPrimeFinderServicer):

	# Overriden method
	def GetLargestPrime(self, request, context):
		'''
		params:
			`request`: `InputRequest` message object from `prime_proto`
		return:
			`UnsignedIntegerResponse` message object from `prime_proto`
		'''
		return get_largest_prime_pb2.UnsignedIntegerResponse(
			status=True,
			message='ok',
			value=request.value
		)
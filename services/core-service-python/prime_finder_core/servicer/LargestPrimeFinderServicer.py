from prime_finder_core.utils.utils import error_request_catching
from prime_finder_core.utils.LargestPrimeFinder import LargestPrimeFinder

from prime_proto.prime_finder_core import get_largest_prime_pb2
from prime_proto.prime_finder_core import get_largest_prime_pb2_grpc

import logging

logger = logging.getLogger()


class LargestPrimeFinderServicer(get_largest_prime_pb2_grpc.LargestPrimeFinderServicer):
	# Overriden method
	def __init__(self):
		self.__prime_finder = LargestPrimeFinder()

	# Overriden method
	@error_request_catching(response_message_class=get_largest_prime_pb2.UnsignedIntegerResponse)
	def GetLargestPrime(self, request, context):
		'''
		params:
			`request`: `InputRequest` message object from `prime_proto`
		return:
			`UnsignedIntegerResponse` message object from `prime_proto`
		'''
		n = request.value
		value = self.__prime_finder.get_lower_largest_prime(n=n)
		logger.warning('Returning result: {value} for input {input}'.format(value=value, input=n))
		return get_largest_prime_pb2.UnsignedIntegerResponse(
			status=True,
			message='ok',
			value=value
		)
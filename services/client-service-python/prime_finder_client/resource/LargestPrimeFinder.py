from prime_finder_client.utils.utils import error_request_catching

from prime_proto.prime_finder_core import get_largest_prime_pb2
from prime_proto.prime_finder_core import get_largest_prime_pb2_grpc

from flask_restful import Resource, reqparse
import sys
import re
import grpc


class LargestPrimeFinder(Resource):
	_UNIT_PATTERN = re.compile(r'^[0-9]+$')
	_MAX_UINT_STR = str(sys.maxsize)
	'''
	The resource for running the largest prime finder
	'''
	def __init__(self, host_address:str):
		self.__parser = reqparse.RequestParser()
		self.__parser.add_argument('n', type=str, help='Input integer number')
		channel = grpc.insecure_channel(host_address)
		self.__stub = get_largest_prime_pb2_grpc.LargestPrimeFinderStub(channel)

	def __is_larger_max(self, n:str):
		if len(n) > len(LargestPrimeFinder._MAX_UINT_STR):
			return True
		if len(n) < len(LargestPrimeFinder._MAX_UINT_STR):
			return False
		for i in range(len(n)):
			if n[i] > LargestPrimeFinder._MAX_UINT_STR[i]:
				return True
			elif n[i] < LargestPrimeFinder._MAX_UINT_STR[i]:
				return False
		return False

	def __validate_input(self, n:str):
		if not LargestPrimeFinder._UNIT_PATTERN.match(n):
			raise Exception('Invalid unsigned integer pattern: {value}'.format(value=n))
		if self.__is_larger_max(n=n):
			raise Exception('Input must be in range [0, {max_int}): {value}'.format(max_int=LargestPrimeFinder._MAX_UINT_STR, value=n))

	# Overriden method
	@error_request_catching()
	def get(self):
		'''
		input:
			An input integer
		return:
			The largest prime number lower than the input number
		'''
		args = self.__parser.parse_args()
		n = args.n.strip('\n\t\r ')
		self.__validate_input(n=n)

		cur_request = get_largest_prime_pb2.InputRequest(
			value=int(n)
		)

		output = self.__stub.GetLargestPrime(cur_request)
		if not output.status:
			raise Exception(output.message)
		return {'output' : output.value}, 200
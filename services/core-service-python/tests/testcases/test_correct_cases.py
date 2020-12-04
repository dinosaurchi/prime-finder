from prime_proto.prime_finder_core import get_largest_prime_pb2
from prime_proto.prime_finder_core import get_largest_prime_pb2_grpc
from prime_finder_core.global_vars import TEST_CORE_SERVICE_ADDRESS

import unittest
import grpc


def is_prime(n):
	if n <= 1:
		return False
	if n == 2:
		return True

	for i in range(2, n):
		if n % i == 0:
			return False
	return True


class Test(unittest.TestCase):
	def runTest(self):
		channel = grpc.insecure_channel(TEST_CORE_SERVICE_ADDRESS)
		stub = get_largest_prime_pb2_grpc.LargestPrimeFinderStub(channel)

		values = list(range(3, 999))
		values += [
			5223444,
		]
		for i in values:
			cur_request = get_largest_prime_pb2.InputRequest(
				value=i
			)
			output = stub.GetLargestPrime(cur_request)
			self.assertTrue(output.status, 'Must have true status: {v}'.format(v=i))
			self.assertTrue(is_prime(n=output.value), msg='Checking highest lower prime: {j} (n={n})'.format(j=output.value, n=i))

			for j in range(output.value + 1, i):
				self.assertFalse(is_prime(n=j), msg='Checking higher prime: {j} (n={n})'.format(j=j, n=i))
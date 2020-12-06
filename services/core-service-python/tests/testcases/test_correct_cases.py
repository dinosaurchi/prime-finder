from prime_proto.prime_finder_core import get_largest_prime_pb2
from prime_proto.prime_finder_core import get_largest_prime_pb2_grpc
from prime_finder_core.global_vars import TEST_CORE_SERVICE_ADDRESS

from tqdm import tqdm
import unittest
import grpc
import timeit


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

		# Repeated range checking, as we want to make sure that the algorithm output is deterministic, given an arbitrary input value
		values = list(range(3, 9999))
		values += list(range(3, 9999))
		values += list(range(2000000, 220000, 1234))
		values += list(range(2000000, 208000, 1234))

		# Large input value check
		values += [
			5223444,
			9999999,
			9999991,
			99999999,
		]

		total_time = 0
		for i in tqdm(values):
			cur_request = get_largest_prime_pb2.InputRequest(
				value=i
			)
			start = timeit.default_timer()
			output = stub.GetLargestPrime(cur_request)
			total_time += timeit.default_timer() - start
			self.assertTrue(output.status, 'Must have true status: {v}'.format(v=i))
			self.assertTrue(is_prime(n=output.value), msg='Checking highest lower prime: {j} (n={n})'.format(j=output.value, n=i))

			for j in range(output.value + 1, i):
				self.assertFalse(is_prime(n=j), msg='Checking higher prime: {j} > {i} (n={n})'.format(j=j, i=output.value, n=i))
		print('Total algorithm runtime: {total_time}'.format(total_time=total_time))

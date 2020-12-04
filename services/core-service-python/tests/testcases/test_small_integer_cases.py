from prime_proto.prime_finder_core import get_largest_prime_pb2
from prime_proto.prime_finder_core import get_largest_prime_pb2_grpc
from prime_finder_core.global_vars import TEST_CORE_SERVICE_ADDRESS

import unittest
import grpc



class Test(unittest.TestCase):
	def runTest(self):
		channel = grpc.insecure_channel(TEST_CORE_SERVICE_ADDRESS)
		stub = get_largest_prime_pb2_grpc.LargestPrimeFinderStub(channel)

		for i in [0, 1, 2]:
			cur_request = get_largest_prime_pb2.InputRequest(
				value=i
			)
			output = stub.GetLargestPrime(cur_request)
			self.assertFalse(output.status, 'Must have fail status: {v}'.format(v=i))

			fail_mess = 'ERROR: Cannot find any prime number less than {v}'.format(v=i)
			fail_mess = fail_mess.lower()
			cur_mess = output.message.lower().strip('\r\t\n ')
			self.assertEquals(cur_mess, fail_mess, 'Must have fail message: {v}'.format(v=i))
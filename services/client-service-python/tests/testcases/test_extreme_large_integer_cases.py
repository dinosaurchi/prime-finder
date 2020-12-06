from prime_finder_client.global_vars import TEST_CLIENT_SERVICE_ADDRESS

import unittest
import requests
import sys
import json


class Test(unittest.TestCase):
	def runTest(self):
		sess = requests.Session()

		max_int = sys.maxsize
		large_ints = [
			'9223372036854775808', # sys.maxsize + 1
			'9223372036854775810', # sys.maxsize + 3
			'92233720368543534785810',
			'9243372036855434785810',
			'9243372056543854785810',
			'534539943372056854785810',
		]

		for i in large_ints:
			url = 'http://{address}/largest_prime?n={n}'.format(address=TEST_CLIENT_SERVICE_ADDRESS, n=i)
			res = sess.get(url).content.decode('utf-8')
			res = json.loads(res)
			self.assertIn('error', res, 'Must have error message: {v}'.format(v=i))

			fail_mess = 'ERROR: Input must be in range [0, {max_int}): {v}'.format(max_int=max_int, v=i)
			fail_mess = fail_mess.lower()
			cur_mess = res['error'].lower().strip('\r\t\n ')
			self.assertEqual(cur_mess, fail_mess, 'Must have fail message: {v}'.format(v=i))
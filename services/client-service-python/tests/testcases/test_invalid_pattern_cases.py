from prime_finder_client.global_vars import TEST_CLIENT_SERVICE_ADDRESS

import unittest
import requests
import json


class Test(unittest.TestCase):
	def runTest(self):
		sess = requests.Session()

		invalids = [
			'-1',
			'-9999',
			'-5345435345',
			'-54353454354355345435345ddd',
			'-sadlkasjdasj',
			'-',
			'-a',
			'',
			'43543-',
			'43543?',
			'34 23423 423',
			'34.23423',
			'34,23423',
			'~',
			'!',
		]

		for i in invalids:
			url = 'http://{address}/largest_prime?n={n}'.format(address=TEST_CLIENT_SERVICE_ADDRESS, n=i)
			res = sess.get(url).content
			res = res.decode('utf-8')
			res = json.loads(res)
			self.assertIn('error', res, 'Must have error message: {v}'.format(v=i))

			fail_mess = 'ERROR: Invalid unsigned integer pattern: {v}'.format(v=i)
			fail_mess = fail_mess.lower().strip('\r\t\n ')
			cur_mess = res['error'].lower().strip('\r\t\n ')
			self.assertEquals(cur_mess, fail_mess, 'Must have fail message: {v}'.format(v=i))

		# GET request does not preceive the `+` and ` ` (left and right), it replaces `+` with ` `
		invalids = [
			'+',
			'+ 44 4',
			'44+4',
			'+ ',
			' ',
			'   ',
		]

		for i in invalids:
			url = 'http://{address}/largest_prime?n={n}'.format(address=TEST_CLIENT_SERVICE_ADDRESS, n=i)
			res = sess.get(url).content
			res = res.decode('utf-8')
			res = json.loads(res)
			self.assertIn('error', res, 'Must have error message: {v}'.format(v=i))

			fail_mess = 'ERROR: Invalid unsigned integer pattern: {v}'.format(v=i.replace('+', ' ').strip('\n\r\t '))
			fail_mess = fail_mess.lower().strip('\r\t\n ')
			cur_mess = res['error'].lower().strip('\r\t\n ')
			self.assertEquals(cur_mess, fail_mess, 'Must have fail message: {v}'.format(v=i))
from prime_finder_client.global_vars import TEST_CLIENT_SERVICE_HOST, TEST_CLIENT_SERVICE_PORT, TEST_CORE_SERVICE_HOST, TEST_CORE_SERVICE_PORT, TEST_CORE_SERVICE_ADDRESS
from pathlib import Path

import traceback
import unittest
import os
import argparse
import subprocess
import threading


def wait_until_start(process, start_message:str):
	while True:
		if not process.poll() is None:
			break
		mess = process.stdout.readline().decode('utf-8').strip('\t\r\n ')
		print(mess)
		if mess.lower().startswith(start_message):
			break


parent_dir = Path(__file__).parent
test_dir = os.path.join(parent_dir, 'testcases')

loader = unittest.TestLoader()
alltests = loader.discover(test_dir)


core_process = subprocess.Popen([
		'python',
		'tests/mock/run_mock_service.py',
		'--host', TEST_CORE_SERVICE_HOST,
		'--port', TEST_CORE_SERVICE_PORT,
	],
	stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT
)
wait_until_start(core_process, 'start running mock-core-serivce on'.lower().strip('\r\t\r '))

client_process = subprocess.Popen([
		'python',
		'prime_finder_client/run.py',
		'--host', TEST_CLIENT_SERVICE_HOST,
		'--port', TEST_CLIENT_SERVICE_PORT,
		'--core_host', TEST_CORE_SERVICE_ADDRESS,
	],
	stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT
)
wait_until_start(client_process, '* Running on http'.lower().strip('\r\t\r '))

exit_code = 0
try:
	log_path = os.path.join(parent_dir, 'logs.txt')
	with open(log_path, 'w+') as f:
		test_res = unittest.TextTestRunner(stream=f, verbosity=2).run(alltests)
		if not test_res.wasSuccessful():
			status = 'FAILED'
			exit_code = 1
		else:
			status = 'PASSED'

		print('{status}. Please check {log_path} for detail.'.format(status=status, log_path=os.path.abspath(log_path)))

except Exception as e:
	print(traceback.format_exc())
	print(e)
	exit_code = 1

core_process.kill()
client_process.kill()
threading.Event().wait(2)
print('Core-process pid [{pid}] {status}'.format(pid=core_process.pid, status=core_process.poll()))
print('Client-process pid [{pid}] {status}'.format(pid=client_process.pid, status=client_process.poll()))
exit(exit_code)
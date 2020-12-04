from prime_finder_core.global_vars import TEST_CORE_SERVICE_HOST, TEST_CORE_SERVICE_PORT
from pathlib import Path

import traceback
import unittest
import os
import argparse
import subprocess
import threading


parent_dir = Path(__file__).parent
test_dir = os.path.join(parent_dir, 'testcases')

loader = unittest.TestLoader()
alltests = loader.discover(test_dir)

command = [
	'python',
	'prime_finder_core/run.py',
	'--host', TEST_CORE_SERVICE_HOST,
	'--port', TEST_CORE_SERVICE_PORT
]
core_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True:
	mess = core_process.stdout.readline().decode('utf-8').strip('\t\r\n ')
	print(mess)
	if not core_process.poll() is None:
		break
	if mess.lower().startswith('start running core-serivce on'):
		break

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
threading.Event().wait(1)
print('Core-process pid [{pid}] {status}'.format(pid=core_process.pid, status=core_process.poll()))
exit(exit_code)
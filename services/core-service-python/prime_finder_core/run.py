from prime_finder_core.servicer.LargestPrimeFinderServicer import LargestPrimeFinderServicer

from prime_proto.prime_finder_core import get_largest_prime_pb2_grpc

from concurrent import futures
import grpc
import argparse
import threading
import logging
import sys


if __name__ == '__main__':
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--host", help="Host IP", default='0.0.0.0')
	parser.add_argument("--port", help="Listening port", default='5001')
	parser.add_argument("--log", help="Logging the result output", action='store_true')
	args = parser.parse_args()

	logger = logging.getLogger()

	address = '{host}:{port}'.format(host=args.host, port=args.port)

	server = grpc.server(futures.ThreadPoolExecutor(max_workers=None))
	server.add_insecure_port(address)

	service = LargestPrimeFinderServicer()
	get_largest_prime_pb2_grpc.add_LargestPrimeFinderServicer_to_server(service, server)

	server.start()
	wait_event = threading.Event()
	try:
		logger.warning('Start running core-serivce on {address}'.format(address=address))
		logger.disabled = not args.log
		while True:
			'''
			We must `flush` the `stdout` to avoid being locked:
			- When the parent process (invoked this process via `subprocess`) is trying to call `stdout.readline()`
			- And when using `time.sleep()` or `threading.Event().wait()` in the subprocess
			'''
			sys.stdout.flush()
			wait_event.wait(timeout=0.005)
	except KeyboardInterrupt:
		pass
	server.stop(0.1)
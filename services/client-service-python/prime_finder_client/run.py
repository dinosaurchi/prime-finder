from prime_finder_client.resource.LargestPrimeFinder import LargestPrimeFinder

from flask_restful import Api
from flask import Flask
import argparse
import logging


app = Flask(__name__)
api = Api(app)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--host", help="Host IP", default='0.0.0.0')
	parser.add_argument("--port", help="Listening port", default='5000')
	parser.add_argument("--core_host", help="Prime-Finder's binding address", required=True)
	parser.add_argument("--debug", help="Run with debugging mode", action='store_true')
	args = parser.parse_args()

	api.add_resource(LargestPrimeFinder, '/largest_prime',
		resource_class_kwargs={
			'host_address': args.core_host
		})
	app.run(debug=args.debug, host=args.host, port=args.port)
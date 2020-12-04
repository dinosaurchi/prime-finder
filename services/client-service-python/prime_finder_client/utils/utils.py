import traceback
import logging


logger = logging.getLogger()


def error_request_catching():
	def wrapper(func):
		def arg_wrapper(resource, **args):
			try:
				return func(resource, **args)
			except Exception as e:
				e = 'ERROR: {e}'.format(e=str(e))
				mess = '{exc}\n{e}'.format(
					exc=traceback.format_exc(),
					e=str(e)
				)
				logger.warning(mess)
				return {'error': e}, 404
		return arg_wrapper
	return wrapper
import traceback
import logging

logger = logging.getLogger()



def error_request_catching(response_message_class):
	def wrapper(func):
		def arg_wrapper(service, request, context):
			try:
				response = func(service, request, context)
			except Exception as e:
				e = 'ERROR: {e}'.format(e=str(e))
				mess = '{exc}\n{e}'.format(
					exc=traceback.format_exc(),
					e=str(e)
				)
				logger.warning(mess)
				response = response_message_class(value=0, message=e, status=False)
			return response
		return arg_wrapper
	return wrapper
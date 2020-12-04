import numpy as np


class LargestPrimeFinder:
	def __init__(self):
		pass

	def __is_prime(self, n:int):
		if n <= 1:
			return False
		if n == 2:
			return True
		if n > 2 and n % 2 == 0:
			return False

		max_n = int(np.floor(np.sqrt(n)))
		# Check all the odd numbers
		for i in range(3, 1 + max_n, 2):
			if n % i == 0:
				return False
		return True

	def get_lower_largest_prime(self, n:int):
		original_n = n
		while n > 0:
			n -= 1
			if self.__is_prime(n=n):
				return n
		raise Exception('Cannot find any prime number less than {n}'.format(n=original_n))
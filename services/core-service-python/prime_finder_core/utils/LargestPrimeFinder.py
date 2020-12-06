import numpy as np


class LargestPrimeFinder:
	def __init__(self):
		self.__marked = None
		# Init for the first 10 millions integers as the algorithm
		self.__update_prime_db(n=1e7)

	def __update_prime_db(self, n:int):
		'''
		Sieve_of_Sundaram algorithm
		- Reference: https://en.wikipedia.org/wiki/Sieve_of_Sundaram
		'''
		if n < 3:
			return

		n = int((n - 1) / 2)
		self.__marked = [False] * (n + 1)

		for i in range(1, n + 1):
			j = i
			while True:
				temp = i + j + 2 * i * j
				if temp  > n:
					break
				self.__marked[temp] = True
				j += 1

	def __is_prime(self, n:int):
		if n <= 1:
			return False
		if n == 2:
			return True
		if n > 2 and n % 2 == 0:
			return False

		check_index = int((n - 1) / 2)
		# Part of Sieve_of_Sundaram algorithm
		return not self.__marked[check_index]

	def get_lower_largest_prime(self, n:int):
		original_n = n
		while n > 0:
			n -= 1
			if self.__is_prime(n=n):
				return n
		raise Exception('Cannot find any prime number less than {n}'.format(n=original_n))
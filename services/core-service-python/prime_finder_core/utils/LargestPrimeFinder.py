from tqdm import tqdm
import numpy as np


class LargestPrimeFinder:
	def __init__(self):
		self.__marked = None
		self.__primes = None
		# Init for the first 10 millions integers as the algorithm
		self.__MAX_INT = int(1e7)
		self.__update_prime_db(n=self.__MAX_INT)

	def __update_prime_db(self, n:int):
		'''
		Sieve_of_Sundaram algorithm
		- Reference: https://en.wikipedia.org/wiki/Sieve_of_Sundaram
		'''
		if n < 3:
			return

		n = int((n - 1) / 2)
		self.__marked = [False] * (n + 1)
		self.__primes = [2]

		for i in tqdm(range(1, n + 1), desc='Building marked database'):
			j = i
			while True:
				temp = i + j + 2 * i * j
				if temp  > n:
					break
				self.__marked[temp] = True
				j += 1

		for i in tqdm(range(1, n + 1), desc='Building primes database'):
			if not self.__marked[i]:
				self.__primes.append(i * 2 + 1)

	def __check_prime(self, n:int):
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

	def __is_prime(self, n:int):
		if n <= 1:
			return False
		if n == 2:
			return True
		if n > 2 and n % 2 == 0:
			return False

		check_index = int((n - 1) / 2)
		if check_index >= len(self.__marked):
			# If the input is out of Sieve_of_Sundaram pre-checked list, we simply check prime with the previous algorithm
			return self.__check_prime(n=n)
		# Part of Sieve_of_Sundaram algorithm
		return not self.__marked[check_index]

	def __binary_search(self, left:int, right:int, n:int):
		if left <= right:
			mid = int((left + right) / 2)

			if mid == 0 or mid == len(self.__primes) - 1:
				return self.__primes[mid]

			if self.__primes[mid] == n:
				return self.__primes[mid - 1]

			if self.__primes[mid] < n and self.__primes[mid + 1] > n:
				return self.__primes[mid]

			if n < self.__primes[mid]:
				return self.__binary_search(left, mid - 1, n)

			return self.__binary_search(mid + 1, right, n)

		raise Exception('Invalid binary search: left ({left}) cannot be larger than right ({right}) (n={n})'.format(left=left, right=right, n=n))

	def get_lower_largest_prime(self, n:int):
		if 2 < n <= self.__MAX_INT:
			res = self.__binary_search(0, len(self.__primes) - 1, n)
			if res:
				return res
		else:
			original_n = n
			while n > 0:
				n -= 1
				if self.__is_prime(n=n):
					return n

		raise Exception('Cannot find any prime number less than {n}'.format(n=original_n))
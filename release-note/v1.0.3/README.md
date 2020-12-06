# Overview

This update consists of:

- Speed up `core-service` with `Binary search` on prime database for `primality check`

- Added more unittest testcases for `core-service` due to the new Binary-search update 

Thus, it deserves a version upgrade from `v1.0.2` to `v1.0.3`


# Sieve of Sundaram with Binary search

For the full-algorithm description, please check [algorithm description](services/core-service-python/README.md)

## Prime searching

For the searching, we use `binary-search`

- The searching complexity will be reduced from `O(n)` to `O(log(n))`

```python

primes = [(2 * i + 1) for i in range(2, 1e7) if marked[i] is False]

def binary_search(left:int, right:int, n:int):
  if left <= right:
    mid = int((left + right) / 2)

    if mid == 0 or mid == len(primes) - 1:
      return primes[mid]

    if primes[mid] == n:
      return primes[mid - 1]

    if primes[mid] < n and primes[mid + 1] > n:
      return primes[mid]

    if n < primes[mid]:
      return binary_search(left, mid - 1, n)

    return binary_search(mid + 1, right, n)

  raise Exception()
```

For `N > 1e7`, we use this `O(n)` algorithm:

```python
while n > 0:
  n -= 1
  if is_prime(n=n):
    return n
```

Related:

- 5f83587728a79a74324b4f2e8d4a72c7d4433d27

- 3d74a2969efd8db7e5cc6f31c730f88bfa7bc981
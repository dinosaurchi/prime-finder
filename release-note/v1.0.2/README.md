# Overview

This update consists of:

- Implemented `Sieve of Sundaram` for `core-service`

- Add more unittest testcases for `core-service`

- Fixed some bugs

Thus, it deserves a version upgrade from `v1.0.1` to `v1.0.2`


# Fix bugs

Added option to disable logging for `core-service` to avoid deadlock

- It could happen nondeterministically when triggered as a `subprocess`

Related: 53d55ba


# Updated `core-service` unittest


## Added repeated range checking for `correctness-checking` unittest

We want to make sure that the algorithm output is deterministic, given an arbitrary input value

- As when using `Sieve of Sundaram` algorithm, we also introduce `cache`, it means, the algorithm can be stateful

Related: 0e79f1c


## Added very large input values testcases

Related: 0f70032 




# Sieve of Sundaram primality check

We use [Sieve of Sundaram](https://en.wikipedia.org/wiki/Sieve_of_Sundaram) algorithm to speed up the primality check for the number in range `[3, 1e7]`

- According to this [informal article](https://medium.com/dev-genius/prime-numbers-and-the-sieve-of-eratosthenes-47f192568c8), this algorithm is efficient for `N <= 10 million`

```python
def create_marked(n:int):
  if n < 3:
    return

  n = int((n - 1) / 2)
  marked = [False] * (n + 1)

  for i in range(1, n + 1):
    j = i
    while True:
      temp = i + j + 2 * i * j
      if temp  > n:
        break
      marked[temp] = True
      j += 1
  return marked

marked = create_marked(1e7)

def is_prime(n:int):
  if n <= 1:
    return False
  if n == 2:
    return True
  if n > 2 and n % 2 == 0:
    return False

  check_index = int((n - 1) / 2)
  # Part of Sieve_of_Sundaram algorithm
  return not marked[check_index]
```

For `N > 1e7`, we use this algorithm
```python
def is_prime(n:int):
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
```

It means, we only check the `odd` numbers, because `even` numbers are always not prime
- Except `2`, thus we already checked if `n==2` beforehand

The check runs in range `[3, sqrt(n))`

We can improve the algorithm further with a latter [Sieve of Atkin](https://en.wikipedia.org/wiki/Sieve_of_Atkin) algorithm

Related:

- 3e58922

- 0c84aa7
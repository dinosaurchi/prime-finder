# Core-service for `Largest Primer Finder`


## `RPC` structure

The `RPC` message and service structure are declared in `rpc/protobuf` (`*.proto`)

Currently, we have only one communicating channel using `protobuf`, thus we have only the `get_largest_prime.proto`

```
syntax = "proto3";
package prime_finder_core.get_largest_prime;


message InputRequest {
	uint64 value = 1;
}

message UnsignedIntegerResponse {
	bool status = 1;
	string message = 2;
	uint64 value = 3;	
}

service LargestPrimeFinder {
	rpc GetLargestPrime(InputRequest) returns (UnsignedIntegerResponse);
}
```

It defines the `GetLargestPrime()` `RPC` with the related `I/O` message structure

- Input an `uint64` value (you have to pre-check your input value before adding to the message)

- Return an `uint64` value, with a `status` message
  - If there was some error, the `status==False` and you should check the `message` to know what happened from the service


## Algorithm description

### Prime database pre-built

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


### Prime searching

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


### Future work

We can improve the prime pre-built algorithm further with a latter [Sieve of Atkin](https://en.wikipedia.org/wiki/Sieve_of_Atkin) algorithm


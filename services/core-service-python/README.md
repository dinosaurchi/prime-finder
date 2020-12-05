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

For the very first version of the solution, we simply find the first prime number down from `N` to `2`

To check the `primality` of a number:
```python
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
```

It means, we only check the `odd` numbers, because `even` numbers are always not prime
- Except `2`, thus we already checked if `n==2` beforehand

The check runs in range `[3, sqrt(n))`

We can improve the algorithm further with checking-cache and also using `Sieve of Sundaram` algorithm

- Ref: https://en.wikipedia.org/wiki/Sieve_of_Sundaram
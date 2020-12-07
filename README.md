# Find the largest prime which is less than `N`

This repo implements the solution for this problem as a micro-service


**Highlight:**

- [x] `GET` request `REST-API`

- [x] Micro-service structure (`client-service` and `core-service`)

- [x] Micro-service `RPC` using `protobuf`

- [x] Service's unittests

- [x] Cross-language services's supported

- [x] Git commit history

- [x] Development/deployment documentation

- [x] API documentation

- [x] Code readability and maintainability

- [x] Containerize service with `Docker`

- [x] Host and run on AWS Free Tier instance

- [x] Implement `core-service` algorithm with `Sieve of Sundaram`

- [x] Speed up `core-service` algorithm with `binary search`

**Upcoming:**

- [ ] Use `Golang` (`1.11` or above with module support) to implement `core-service`

- [ ] Support running with a batch of `N`s for `core-service` to speed up

- [ ] Implement `credentials` for `client-service`


## Overview

We have 2 containerized services:

- `core-service`: is where the prime finding process happens

- `client-service`: is the `REST-API` to implement a `GET` request

## Communication

The 2 services communicate via `protobuf`, using `gPRC` to auto-generate the stub and servicers scripts

As using `protobuf`, the `core-service` can be implemented in a different programming language to the `client-service`

- It eases the long-term development for both maintenance and improvement

- For instance, we can speed up the `core-service` with a new implementation with `Golang` or `C++`

## Testing

With the `micro-service` structure, each service can be tested independently, thus we can easily scale-up the whole service

- Hiring more developers

- Working on each service simultaneously

The `client-serivce` is tested using a `mock-core-service` to pretend having the result from the `core-service`

The `core-service` tests itself via its implemented `RPC`


## Containerization

Those `micro-services` are containerized using `Docker`


## User tutorial


### AWS Host

Currently the service is running on an `AWS` instance at:
```
http://54.179.177.247:5000/largest_prime
```

### Client API

From your web-browser, go to the following address
```
http://<running_host>:<running_port>/largest_prime?n=<input_number>
```

For instance:
```
GET http://54.179.177.247:5000/largest_prime?n=3000

{"output" : 2999}


GET http://54.179.177.247:5000/largest_prime?n=7

{"output" : 5}


GET http://54.179.177.247:5000/largest_prime?n=2

{"error": "ERROR: ERROR: Cannot find any prime number less than 2"}


GET http://54.179.177.247:5000/largest_prime?n=-1344

{"error": "ERROR: Invalid unsigned integer pattern: -1344"}


GET http://54.179.177.247:5000/largest_prime?n=99999999999999999999999999

{"error": "ERROR: Input must be in range [0, 9223372036854775807): 99999999999999999999999999"}
```

### Build and run the service

Clone expected version from this repo: [`prime-finder`](https://github.com/dinosaurchi/prime-finder)

Before building the service, we have to add the unix user to the `docker` group
```sh
$ sudo groupadd docker
$ sudo usermod -a -G docker $USER
```

Then, reboot your instance

Run the following command:
```sh
$ ./build.sh
```

This script runs the `COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build` with the pre-loaded environment variables

To change build configuration, edit the default `.env` (can be different on different hosts):
```
BUILD_VERSION=1.0.0

# Directories
SERVICES_DIR=./services
PROTO_DIR=./rpc
CORE_SERVICE_DIR=./services/core-service-python
CLIENT_SERVICE_DIR=./services/client-service-python

# Ports
CLIENT_SERVICE_PORT=5000
CORE_SERVICE_PORT=5001
```

Run the following command to startup all related services:
```sh
$ docker-compose up -d
```


## Development tutorial

### `RPC` structure

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

### Generating cross-language `RPC`

First of all, update the `*.proto` if you want to change something

Then, run the following commands to generate language-specific `RPC`:
```
$ ./rpc/build_proto.sh
```

Note that which languages to be generated depends on what is your build's declaration in the `./rpc/build_proto.sh` script.
- When generated, it keeps the `protobuf` directory structure

For instance, here is the `gRPC` build script for `Python`:
```sh
python -m grpc_tools.protoc -I ./protobuf --grpc_python_out ./python --python_out ./python ./protobuf/**/**/*.proto
find ./python -type d -exec touch {}/__init__.py \;
```


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


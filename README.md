# Find the largest prine which is less than `N`

This repo implements the solution for this problem as a micro-service


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

### Build

Clone expected version from this repo: [`stably-interview`](https://github.com/dinosaurchi/stably-interview)

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

### Run

Run the following command to startup all related services:
```sh
$ docker-compose up -d
```

### Client API

From your web-browser, go to the following address
```
http://<running_host>:<running_port>/largest_prime?n=<input_number>
```

For instance:
```
GET http://127.0.0.1:5000/largest_prime?n=3000

{"output" : 2999}


GET http://127.0.0.1:5000/largest_prime?n=7

{"output" : 5}


GET http://127.0.0.1:5000/largest_prime?n=2

{"error": "ERROR: ERROR: Cannot find any prime number less than 2"}


GET http://127.0.0.1:5000/largest_prime?n=-1344

{"error": "ERROR: Invalid unsigned integer pattern: -1344"}


GET http://127.0.0.1:5000/largest_prime?n=99999999999999999999999999

{"error": "ERROR: Input must be in range [0, 9223372036854775807): 99999999999999999999999999"}
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

### Algorithm description

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
# Overview

This update consists of:

- Tutorial on how to use the deployed service on `AWS` instance

- Fixed some build bugs

Because it is all about fixing and deploying, thus it deserves a version upgrade:

- `v1.0.0` -> `v1.0.1`


# AWS Host

Currently the service is running on an `AWS` instance at:
```
http://54.179.177.247:5000/largest_prime
```

## Usage

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
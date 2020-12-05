# REST-API service for `Largest Primer Finder`


## AWS Host

Currently the service is running on an `AWS` instance at
```
http://54.179.177.247:5000/largest_prime
```

## Client API

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
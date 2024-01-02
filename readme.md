# history data microservices

for recieving klines data and store it to database

## services

1. api_service
2. request_service
3. data_management_service
4. kafka service

### api_service

For recieving klines by needed period from binance api
result is to send mini periods to next microservice "request_service" through kafka message broker
service generate mini periods for requests because binance api have limits per each request.
also service check unique mini periods according data that stored in redis.

### request_service

service recieves message from kafka and according to message parameters makes request to binance api
next send response to data_management_service using message brocker

### data_management_service

service recieves message from message brocker and save data in mongo. also is save process to redis for limit same requests (need to api_service)

### kafka service

service just create message brocker

## How to run?

1. run container into kafka_service
2. run databases containers into data_management_service and make init mongodb
3. run install all requirements in services and run `python main.py` into all services

# TODO

Unite docker-compse files into one
and dockerize all services

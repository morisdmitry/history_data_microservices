# data_management_service

for saving in data in databases
recieve message from kafka and save data in databases

## How to run?

need to implement commands:
`make up_redis`
`make up_mongo`

after running mongo container need to create indexes:
`python init/mongo_init.py`

to stop:
`make down_redis`
`make down_mongo`

## issues

need to change method `TimeoutError` from aioredis

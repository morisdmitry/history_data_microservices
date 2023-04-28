import redis
import json

# Connect to Redis
r = redis.Redis(host="localhost", port=6377, db=0)

# Define the timestamp range prefix and key pattern


needed_value = "1649361871000"
key_pattern = f"hdata:1s:*"

# Retrieve the Redis keys that match the key pattern and filter by timestamp range

keys = []
for key in r.keys(key_pattern):
    start_ts = key.decode().split(":")[1]
    end_ts = key.decode().split(":")[2]
    if start_ts <= needed_value <= end_ts:
        keys.append(key.decode())

print(f"keys {keys}")

# Retrieve the JSON data from Redis for each matching key
json_data = [json.loads(r.execute_command("GET", key)) for key in keys]

# Print the sorted data
print(json_data)

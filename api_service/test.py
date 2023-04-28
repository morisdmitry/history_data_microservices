from datetime import datetime, time


def generate_integers(start_int, end_int, step, limit):
    integers = []
    limit = limit * 1000
    while start_int <= end_int and start_int + limit <= end_int:
        integers.append([start_int, start_int + limit])
        start_int += step + limit
    if start_int <= end_int:
        integers.append([start_int, end_int])
    return integers


def generate_integers2(start_int, end_int, step):
    limit = 5
    integers = []
    count = 1
    left_cursor = start_int
    for i in range(start_int, end_int, step):
        # print("i", i)
        if left_cursor == None:
            left_cursor = i

        if count >= limit:
            integers.append({"left": left_cursor, "right": i})
            left_cursor = None
            count = 0
        count += 1
    if not integers:
        return [{"left": start_int, "right": end_int}]
    if integers and integers[-1]["right"] < end_int:
        integers.append({"left": integers[-1]["right"] + step, "right": end_int})

    return integers


# integers = generate_integers(10, 20, 2, 4)
# integers = generate_integers2(1680825600000, 1681257600000, 14400000)
# print(integers)
# integers2 = generate_integers2(1680739200000, 1681257600000, 14400000)
# print(integers2)


integers = generate_integers2(500, 620, 12)
print(integers)
integers2 = generate_integers2(400, 620, 12)
print(integers2)


# /////////////////////////

# import requests


# for range in integers:
#     get_klines_url = "https://api.binance.com/api/v3/klines"
#     params = {
#         f"symbol": "ETHBUSD",
#         "startTime": range["left"],
#         "endTime": range["right"],
#         "interval": "4h",
#         "limit": 5,
#     }

#     response = requests.get(get_klines_url, params=params)

#     print(f"response {response}")
#     print(f"response {response.json()}")

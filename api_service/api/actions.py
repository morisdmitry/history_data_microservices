from datetime import datetime, time


async def get_only_new_periods(database, period, periods,  symbol):
    key_pattern = f"keys:{symbol}:{period}"

    keys = []
    db_keys = await database.keys(key_pattern)
    if not db_keys:
        return periods

    results = await database.execute_command("SMISMEMBER", key_pattern, *periods)
    print(f">>> {len(results)}")

    for i in range(len(periods)):
        if results[i] == 0:
            keys.append(periods[i])

    print(f"get_only_new_periods {len(keys)}")
    return keys


# async def get_only_new_periods(database, period, periods):
#     key_pattern = f"hdata:{period}:*"

#     keys = []

#     db_keys = await database.keys(key_pattern)
#     if not db_keys:
#         return periods

#     for time_period in periods:
#         if (
#             f'hdata:{time_period["start_time"]}:{time_period["end_time"]}'
#             not in db_keys
#         ):
#             keys.append(time_period)

#     print(f"keys {len(keys)}")
#     return keys


# async def get_only_new_periods(database, period, periods):
#     key_pattern = f"hdata:{period}:*"

#     keys = []

#     db_keys = await database.keys(key_pattern)
#     if not db_keys:
#         return periods

#     for key in db_keys:
#         print(f"key {key}")
#         start_ts = key.decode().split(":")[2]
#         end_ts = key.decode().split(":")[3]

#         for time_period in periods:
#             print(f"time_period {time_period}")
#             print(f"start_ts {start_ts}")
#             print(f"end_ts {end_ts}")
#             if (
#                 start_ts != time_period["start_time"]
#                 and end_ts != time_period["end_time"]
#             ):
#                 keys.append(time_period)

#     print(f"keys {len(keys)}")
#     return keys


def get_timestamp(date):
    datetime_obj = datetime.combine(date, time.min)
    return int(datetime_obj.timestamp()) * 1000


def get_periods_between(start_date, end_date, step):
    # there is prpblem with sync data periods
    # [{'left': 500, 'right': 548}, {'left': 560, 'right': 608}, {'left': 620, 'right': 620}]
    # [{'left': 400, 'right': 448}, {'left': 460, 'right': 508}, {'left': 520, 'right': 568}, {'left': 580, 'right': 620}]

    print(f"step {step}")
    step = step * 1000
    start_date = get_timestamp(start_date)
    end_date = get_timestamp(end_date)

    left_cursor = start_date

    limit = 1000
    periods = []
    count = 0
    for i in range(start_date, end_date, step):
        count += 1
        if left_cursor == None:
            left_cursor = i

        if count >= limit:
            periods.append(f"{left_cursor}:{i + step}")
            left_cursor = None
            count = 0

    if not periods:
        return [f"{start_date}:{end_date}"]
    if periods and int(periods[-1].split(":", 1)[1]) < end_date:
        print(">>>>>>>>>>>>>>>>")
        periods.append(f'{int(periods[-1].split(":", 1)[1])}:{end_date}')
    print(f"get_periods_between > {len(periods)}")
    print(f"get_periods_between > {periods}")
    return periods


def period_in_seconds(time_period):
    time_periods = [
        {"key": "1s", "in_seconds": 1},
        {"key": "1m", "in_seconds": 60},
        {"key": "3m", "in_seconds": 180},
        {"key": "5m", "in_seconds": 300},
        {"key": "15m", "in_seconds": 900},
        {"key": "30m", "in_seconds": 1800},
        {"key": "1h", "in_seconds": 3600},
        {"key": "2h", "in_seconds": 7200},
        {"key": "4h", "in_seconds": 14400},
        {"key": "6h", "in_seconds": 21600},
        {"key": "8h", "in_seconds": 28800},
        {"key": "12h", "in_seconds": 43200},
        {"key": "1d", "in_seconds": 86400},
        {"key": "3d", "in_seconds": 259200},
        {"key": "1w", "in_seconds": 604800},
        {"key": "1M", "in_seconds": 2592000},
    ]

    # if time_period in time_periods:
    #     return time_periods[time_period]

    for tp in time_periods:
        if time_period == tp["key"]:
            return tp["in_seconds"]
    return None

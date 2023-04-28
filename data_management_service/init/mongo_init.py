import asyncio
import motor.motor_asyncio
import bson
import re

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["application"]


async def create_index():
    # Create index on starttime:endtime key
    await db.records.create_index("starttime:endtime", unique=True)
    await db.records.create_index("starttime")
    await db.records.create_index("endtime")


async def search_documents():
    start_time = 1658413000000
    end_time = 1677967100000

    # start_time = "1675573000000"
    # end_time = "1675573999000"
    query = {
        "starttime": {"$lte": start_time},
        "period": "4h",
    }

    # test = await db.records.find(query, limit=1).explain("executionStats")
    # print(f"test {test}")
    # test = await db.records.find(query)
    res1 = []
    async for document in db.records.find(
        query,
    ):
        print(">>>>> 1", document["starttime:endtime"])
        res1.append(document)

    print(f'test>> {res1[-1]["starttime:endtime"]}')
    # if test:
    #     print(f'test {test["starttime:endtime"]}')

    start_time = 1658413000000
    end_time = 1677967100000
    query = {
        "endtime": {"$gte": end_time},
        "period": "4h",
    }

    # test = await db.records.find_one(query)
    # if test:
    #     print(f'test {test["starttime:endtime"]}')
    async for document in db.records.find(query, limit=1):
        print(">>>>2", document["starttime:endtime"])
    # async for document in db.records.find(query, limit=1):
    #     print(document["starttime:endtime"])


async def main():
    await create_index()
    # await search_documents()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from pyle38 import Tile38


async def main():
    tile38 = Tile38(url="redis://localhost:9851", follower_url="redis://localhost:9851")

    print("adding entry to tile38")
    response = await tile38.set("fleet", "truck").point(52.25, 13.37).exec()
    print(response.dict())

    print("querying tile38")
    response = await tile38.follower()\
        .within("fleet")\
        .circle(52.25, 13.37, 1000)\
        .asObjects()

    print(response.dict())
    print("done")

asyncio.run(main())

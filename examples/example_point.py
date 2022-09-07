import asyncio

from pyle38 import Tile38


async def main():
    tile38 = Tile38(url="redis://localhost:9851", follower_url="redis://localhost:9851")

    # Assuming radius is in metres?
    response = (
        await tile38.within("ps")
        .limit(1_000_000)
        .circle(lat=40.72716031, lon=-73.88429579, radius=5_000)
        .asObjects()
    )

    out = response.dict()
    print(f"Returned {len(out['objects']):,} objects in {out['elapsed']}")
    await tile38.quit()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import json

from pyle38 import Tile38
from shapely import wkt
from shapely.geometry import mapping


async def main():
    tile38 = Tile38(url="redis://localhost:9851", follower_url="redis://localhost:9851")

    # Querying a small Polygon
    broadway = wkt.loads(
        """
        Polygon ((
            -73.98847105508848188 40.7482867876015078,
            -73.98789783821904109 40.7481299712272147,
            -73.988996503885474 40.74299101466307604,
            -73.9893149577018221 40.74328054389826548,
            -73.98847105508848188 40.7482867876015078
        ))"""
    )

    response = (
        await tile38.within("ps").limit(1_000_000).object(mapping(broadway)).asObjects()
    )
    out = response.dict()
    print(f"Returned {len(out['objects']):,} objects in {out['elapsed']}")
    await tile38.quit()


if __name__ == "__main__":
    asyncio.run(main())

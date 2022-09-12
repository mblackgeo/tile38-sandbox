import argparse
import asyncio
from enum import Enum
from pathlib import Path

import geopandas as gpd
from pyle38 import Tile38
from shapely import wkt
from shapely.geometry import mapping


class QueryType(Enum):
    SMALL = 1
    LARGE = 2
    POINT = 3

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def argparse(s: str) -> "QueryType":
        try:
            return QueryType[s.upper()]
        except KeyError:
            return s


async def main(query: QueryType):
    """Perform an example query against a populated Tile38 data store

    Parameters
    ----------
    query : QueryType
        Type of query to perform
    """
    tile38 = Tile38(url="redis://localhost:9851", follower_url="redis://localhost:9851")

    if query == QueryType.SMALL:
        # A small polygon around part of Broadway
        geometry = wkt.loads(
            "Polygon (( "
            "-73.98847105508848188 40.7482867876015078, "
            "-73.98789783821904109 40.7481299712272147, "
            "-73.988996503885474 40.74299101466307604, "
            "-73.9893149577018221 40.74328054389826548, "
            "-73.98847105508848188 40.7482867876015078 "
            "))"
        )
        out = (
            await tile38.intersects("ps")
            .limit(1_000_000)
            .object(mapping(geometry))
            .asIds()
        )

    elif query == QueryType.LARGE:
        # A large buffered polygon that covers a long route through NYC
        gdf = gpd.read_file(
            Path(__file__).parent.parent / "data" / "long-route-200m-buffer.geojson"
        )
        geometry = gdf.geometry.iloc[0]
        out = (
            await tile38.intersects("ps")
            .limit(1_000_000)
            .object(mapping(geometry))
            .asIds()
        )

    elif query == QueryType.POINT:
        # A Point and radius query
        out = (
            await tile38.intersects("ps")
            .limit(1_000_000)
            .circle(lat=40.72716031, lon=-73.88429579, radius=3000)
            .asIds()
        )

    print(out)
    print(f"Returned {len(out.ids)} objects in {out.elapsed}")
    await tile38.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    req = parser.add_argument_group("required arguments")
    req.add_argument(
        "-q",
        "--query-type",
        type=QueryType.argparse,
        help="Type of Query to perform.",
        required=True,
        choices=list(QueryType),
    )

    args = parser.parse_args()

    asyncio.run(main(query=QueryType(args.query_type)))

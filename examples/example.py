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
    DONUT = 4

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


async def main(query: QueryType, radius: float) -> None:
    """Perform an example query against a populated Tile38 data store

    Parameters
    ----------
    query : QueryType
        Type of query to perform
    radius : float
        Radius if querying a point
    """
    tile38 = Tile38(url="redis://localhost:9851")

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
            .circle(lat=40.72716031, lon=-73.88429579, radius=radius)
            .asIds()
        )

    elif query == QueryType.DONUT:
        # A Polygon with an inner ring
        gdf = gpd.read_file(Path(__file__).parent.parent / "data" / "donut.geojson")
        geometry = gdf.geometry.iloc[0]
        out = (
            await tile38.within("ps").limit(1_000_000).object(mapping(geometry)).asIds()
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

    # optional args
    parser.add_argument(
        "-r",
        "--radius",
        type=float,
        help="Radius to buffer (meters), if `--query-type point`",
        required=False,
        default=3000,
    )

    args = parser.parse_args()

    asyncio.run(main(query=QueryType(args.query_type), radius=args.radius))

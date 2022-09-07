import pytest
from pyle38 import Tile38
from shapely import wkt
from shapely.geometry import mapping


@pytest.mark.asyncio
async def small_polygon_intersect(tile38: Tile38):
    ply = wkt.loads(
        """
        Polygon ((
            -73.98847105508848188 40.7482867876015078,
            -73.98789783821904109 40.7481299712272147,
            -73.988996503885474 40.74299101466307604,
            -73.9893149577018221 40.74328054389826548,
            -73.98847105508848188 40.7482867876015078
        ))"""
    )
    await tile38.within("ps").limit(1_000_000).object(mapping(ply)).asObjects()
    await tile38.quit()


@pytest.mark.asyncio
async def large_radius_intersect(tile38: Tile38):
    await tile38.within("ps").limit(1_000_000).circle(
        lat=40.72716031,
        lon=-73.88429579,
        radius=5_000,
    ).asObjects()
    await tile38.quit()


def test_polygon(aio_benchmark, tile38):
    aio_benchmark(lambda: small_polygon_intersect(tile38))


def test_point(aio_benchmark, tile38):
    aio_benchmark(lambda: large_radius_intersect(tile38))

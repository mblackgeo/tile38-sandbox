import pytest
from pyle38 import Tile38
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry


async def polygon(geom: BaseGeometry) -> None:
    conn = Tile38(url="redis://localhost:9851")
    res = await conn.within("ps").limit(1_000_000).object(mapping(geom)).asObjects()
    assert len(res.dict()) > 0
    await conn.quit()


@pytest.mark.benchmark(min_rounds=10)
def test_donut(donut, aio_benchmark):
    aio_benchmark(polygon, donut)


@pytest.mark.benchmark(min_rounds=10)
def test_route(route, aio_benchmark):
    aio_benchmark(polygon, route)

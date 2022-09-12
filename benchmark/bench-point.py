import pytest
from pyle38 import Tile38


async def radius(r: float) -> None:
    conn = Tile38(url="redis://localhost:9851")
    res = (
        await conn.within("ps")
        .limit(1_000_000)
        .circle(lat=40.72716031, lon=-73.88429579, radius=r)
        .asObjects()
    )
    assert len(res.dict()) > 0
    await conn.quit()


@pytest.mark.benchmark(min_rounds=10)
def test_radius_850m(aio_benchmark):
    aio_benchmark(radius, 850)


@pytest.mark.benchmark(min_rounds=10)
def test_radius_1km(aio_benchmark):
    aio_benchmark(radius, 1000)


@pytest.mark.benchmark(min_rounds=10)
def test_radius_3km(aio_benchmark):
    aio_benchmark(radius, 3000)


@pytest.mark.benchmark(min_rounds=10)
def test_radius_5km(aio_benchmark):
    aio_benchmark(radius, 5000)


@pytest.mark.benchmark(min_rounds=10)
def test_radius_5km(aio_benchmark):
    aio_benchmark(radius, 5000)

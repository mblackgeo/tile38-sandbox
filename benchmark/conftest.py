# Benchmark fixtures for pytest-asyncio
# https://github.com/ionelmc/pytest-benchmark/issues/66#issuecomment-1137005280
from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Polygon


@pytest.yield_fixture(scope="function")
def aio_benchmark(benchmark):
    import asyncio
    import threading

    class Sync2Async:
        def __init__(self, coro, *args, **kwargs):
            self.coro = coro
            self.args = args
            self.kwargs = kwargs
            self.custom_loop = None
            self.thread = None

        def start_background_loop(self) -> None:
            asyncio.set_event_loop(self.custom_loop)
            self.custom_loop.run_forever()

        def __call__(self):
            evloop = None
            awaitable = self.coro(*self.args, **self.kwargs)
            try:
                evloop = asyncio.get_running_loop()
            except:
                pass
            if evloop is None:
                return asyncio.run(awaitable)
            else:
                if (
                    not self.custom_loop
                    or not self.thread
                    or not self.thread.is_alive()
                ):
                    self.custom_loop = asyncio.new_event_loop()
                    self.thread = threading.Thread(
                        target=self.start_background_loop, daemon=True
                    )
                    self.thread.start()

                return asyncio.run_coroutine_threadsafe(
                    awaitable, self.custom_loop
                ).result()

    def _wrapper(func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            benchmark(Sync2Async(func, *args, **kwargs))
        else:
            benchmark(func, *args, **kwargs)

    return _wrapper


@pytest.fixture(scope="session")
def route() -> Polygon:
    gdf = gpd.read_file(
        Path(__file__).parent.parent / "data" / "route-buffered.geojson"
    )
    return gdf.geometry.iloc[0]


@pytest.fixture(scope="session")
def donut() -> Polygon:
    gdf = gpd.read_file(Path(__file__).parent.parent / "data" / "donut.geojson")
    return gdf.geometry.iloc[0]

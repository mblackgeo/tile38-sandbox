# Benchmark fixtures for pytest-asyncio
# https://github.com/ionelmc/pytest-benchmark/issues/66#issuecomment-1137005280

import asyncio

import pytest_asyncio


@pytest_asyncio.fixture
async def aio_benchmark(benchmark, event_loop):
    def _wrapper(func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            @benchmark
            def _():
                return event_loop.run_until_complete(func(*args, **kwargs))
        else:
            benchmark(func, *args, **kwargs)

    return _wrapper

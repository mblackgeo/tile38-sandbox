import pytest
import pytest_asyncio
from pyle38 import Tile38


@pytest_asyncio.fixture()
async def tile38():
    conn = Tile38(url="redis://localhost:9851")
    yield conn
    await conn.quit()

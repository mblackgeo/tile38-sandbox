import pytest
from pyle38 import Tile38


@pytest.mark.asyncio
async def test_large_radius_intersect(tile38: Tile38):
    # add some new fields so we can test filtering
    # fields MUST BE NUMERIC ONLY
    await (
        tile38.set("fleet", "truck1")
        .fields({"maxSpeed": 90, "milage": 90000})
        .point(33.5123, -112.2693)
        .exec()
    )

    await (
        tile38.set("fleet", "truck2")
        .fields({"maxSpeed": 30, "milage": 30000})
        .point(33.5123, -112.2693)
        .exec()
    )

    # check we have at least two trucks in the fleet
    res = await tile38.scan("fleet").asCount()
    assert res.count >= 2

    # Query for a truck going between 80 and 100
    res = (
        await tile38.nearby("fleet")
        .where("maxSpeed", min=80, max=100)
        .point(33.5124, -112.2694)
        .asObjects()
    )

    assert res.count == 1
    assert res.objects[0].id == "truck1"


@pytest.mark.asyncio
async def test_matching(tile38: Tile38):
    await (tile38.set("fleet", "van1").point(33.5123, -112.2693).exec())
    await (tile38.set("fleet", "car1").point(33.5123, -112.2693).exec())

    # Query only for vans
    res = (
        await tile38.nearby("fleet")
        .match("van*")
        .point(33.51244, -112.26944)
        .asObjects()
    )

    assert res.count == 1
    assert res.objects[0].id == "van1"

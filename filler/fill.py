import os
from pathlib import Path

import geopandas as gpd
from pyle38 import Tile38


def main(tile38_host: str, id_field: str) -> None:
    """Read any Geopackage files present in /data and put them in tile38"""
    tile38 = Tile38(url=tile38_host)

    for file in Path("/data").glob("*.gpkg"):
        gdf = gpd.read_file(file)
        for row in gdf.itertuples():
            # make a temporary GeoDataFrame from this row so we can expose
            # the GeoJSON interface for the geometry
            # TODO probably a nicer way to do this
            _tmp = gpd.GeoDataFrame({"geometry": row.geometry})

            # Insert the entry into Tile38
            tile38.set(key=file.name, id=getattr(row[id_field])).object(_tmp.__geo_interface__["geometry"])



if __name__ == "__main__":
    main(
        tile38_host=os.environ.get("FILLER__TILE38_HOST", "redis://tile38:9851"),
        id_field=os.environ.get("FILLER__ID_FIELD", "rid")
    )

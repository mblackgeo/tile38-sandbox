import os
from pathlib import Path

import geopandas as gpd
from pyle38 import Tile38
from shapely.geometry import mapping


def main(tile38_host: str, id_field: str) -> None:
    """Read any Geopackage files present in /data and put them in tile38"""
    tile38 = Tile38(url=tile38_host)

    for file in Path("/data").glob("*.gpkg"):
        gdf = gpd.read_file(file)

        for row in gdf.itertuples():
            tile38\
                .set(key=file.name, id=getattr(row[id_field]))\
                .object(mapping(row.geometry))



if __name__ == "__main__":
    main(
        tile38_host=os.environ.get("FILLER__TILE38_HOST", "redis://tile38:9851"),
        id_field=os.environ.get("FILLER__ID_FIELD", "rid")
    )

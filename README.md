# tile38-sandbox
Investigations of using [Tile38](https://github.com/tidwall/tile38), the fast in-memory geospatial data store, for performing spatial joins.

## Getting started

First create a new virtual environment and install the dependencies

```shell
mkvirtualenv --python=/usr/bin/python3.8 tile38

make install
```

Next prepare some data for insert to Tile38:

* Place GeoPackage files (.gpkg) in the `/data` directory
* The [`fill.py`](/filler/fill.py) script will pick up these files
* They will be ingested and put in Tile38, the following env vars are used:
    * `FILLER__ID_FIELD`: the name of the field in the Geopackage that contains the ID
    * `FILLER__KEY`: the key used
    * These can be customed by making a `.env` file, following `.env.example`

Finally, startup Tile38 and run the filler:

```shell
make run  # or docker-compose up --build
```

After a few minutes (depending on the size of the data to be ingested), you should see a log message that the filler has finished. Queries can now be made against this data using [`pyle38`](https://github.com/iwpnd/pyle38). See [`examples`](/examples/) for more.

## Benchmarks

Some simple benchmarks were implemented (following the [`examples`](/examples/)), assuming Tile38 has been filled with data in New York City (see [`bench.py`](/benchmark/bench.py)). These are two queries, one to perform a spatial join with a polygon (roughly a bounding box around Broadway), and second to perform a larger query of all data within a 3 km radius. The results are shown below:

* `test_polygon` returns 16 objects
* `test_point` returns 10,217 objects

```
-------------------------------------------- benchmark: 2 tests --------------------------------------------
Name (time in ms)         Mean              Median                 Min                 Max            Rounds
------------------------------------------------------------------------------------------------------------
test_polygon            1.6955 (1.0)        1.5974 (1.0)        1.4717 (1.0)       10.9796 (1.0)         234
test_point            292.4011 (172.45)   294.6022 (184.43)   275.7353 (187.36)   307.7656 (28.03)        10
------------------------------------------------------------------------------------------------------------
```

Tested on an Intel i7-1165G7.

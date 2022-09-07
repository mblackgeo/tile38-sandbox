# tile38-sandbox
Investigations of using [Tile38](https://github.com/tidwall/tile38) (the fast in-memory geospatial data store)

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

Some simple benchmarks were implemented (following the [`examples`](/examples/)), assuming Tile38 has been filled with data in New York City (see [`bench.py`](/benchmark/bench.py)). These are two queries, one to perform a spatial join with a polygon (roughly a bounding box around Broadway), and second to perform a larger query of all data within a 5 km radius. The results are shown below:

* `test_polygon` returns 16 objects
* `test_radius` returns 28,762 objects

```
----------------------------------------- benchmark: 2 tests ----------------------------------------
Name (time in us)        Min                Max              Mean            Median            Rounds
-----------------------------------------------------------------------------------------------------
test_polygon          1.5200 (1.0)      29.2900 (1.21)     1.6617 (1.0)      1.6155 (1.0)       17382
test_point            1.5270 (1.00)     24.2540 (1.0)      1.8149 (1.09)     1.6160 (1.00)      51170
-----------------------------------------------------------------------------------------------------
```

Tested on an Intel i7-1165G7.

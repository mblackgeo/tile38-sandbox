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

After a few minutes (depending on the size of the data to be ingested), you should see a log message that the filler has finished. Queries can now be made against this data using [`pyle38`](https://github.com/iwpnd/pyle38). See [`examples`](/examples/) for more or run `make example`.

## Benchmarks

Some simple benchmarks were implemented (following the [`examples`](/examples/)), assuming Tile38 has been filled with data in New York City (see [`bench.py`](/benchmark/bench.py)). Firstly there are some increasing radius queries (`make bench-point`):

* `test_radius_850m` returns 154 objects
* `test_radius_1km` returns 344 objects
* `test_radius_3km` returns 10,441 objects
* `test_radius_5km` returns 29,023 objects

```
-------------------------------------------- benchmark: 4 tests --------------------------------------------
Name (time in ms)         Mean              Median                 Min                 Max            Rounds
------------------------------------------------------------------------------------------------------------
test_radius_850m        5.9744 (1.0)        5.3475 (1.0)        5.1099 (1.0)       21.9919 (1.0)         120
test_radius_1km        11.2427 (1.88)      10.1879 (1.91)       9.5091 (1.86)      25.9977 (1.18)         89
test_radius_3km       300.2658 (50.26)    300.1839 (56.14)    283.2725 (55.44)    319.6502 (14.53)        10
test_radius_5km       936.0482 (156.68)   940.5802 (175.89)   867.4683 (169.76)   972.7046 (44.23)        10
------------------------------------------------------------------------------------------------------------
```

Secondly there are queries against a polygon with an inner ring (donut) and against a long buffered route through NYC (`make bench-polygon`):

* `test_donut` returns 3,857 objects
* `test_route` returns 5,177 objects

```
-------------------------------------------- benchmark: 2 tests --------------------------------------------
Name (time in ms)         Mean              Median                 Min                 Max            Rounds
------------------------------------------------------------------------------------------------------------
test_donut             92.9373 (1.0)       94.9443 (1.0)       82.6249 (1.0)      105.8971 (1.0)          10
test_route            131.9810 (1.42)     134.7894 (1.42)     117.7069 (1.42)     141.0894 (1.33)         10
------------------------------------------------------------------------------------------------------------
```

Tested on an Intel i7-1165G7.

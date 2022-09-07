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

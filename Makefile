.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: install
install:  ## Install dev requirements into the current python environment
	pip install -r requirements.txt

.PHONY: run
run:  ## Run the Tile38 data store locally with docker-compose
	docker compose up --build

.PHONY: example
example:  ## Run an example query against a populated Tile38 data store
	python examples/example.py -q donut

.PHONY: bench-point
bench-point:  ## Run the benchmarks against a point w/ radius
	pytest benchmark/bench-point.py --disable-warnings --benchmark-columns="mean, median, min, max, rounds"

.PHONY: bench-polygon
bench-polygon:  ## Run the benchmarks against polygons
	pytest benchmark/bench-polygon.py --disable-warnings --benchmark-columns="mean, median, min, max, rounds"

.PHONY: test
test:  ## Run some unit tests (requires Tile38 to be up)
	pytest --disable-warnings tests/
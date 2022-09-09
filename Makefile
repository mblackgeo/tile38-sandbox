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
	python examples/example_polygon.py

.PHONY: bench
bench:  ## Run the benchmarks
	pytest benchmark/bench.py --disable-warnings --benchmark-columns="min, max, mean, median, rounds"

.PHONY: test
test:  ## Run some unit tests (requires Tile38 to be up)
	pytest --disable-warnings tests/
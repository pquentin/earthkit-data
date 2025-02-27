PROJECT := earthkit-data
CONDA := conda
CONDAFLAGS :=
COV_REPORT := html

default: qa unit-tests type-check

qa:
	pre-commit run --all-files

unit-tests:
	python -m pytest -vv -m 'not notebook' --cov=. --cov-report=$(COV_REPORT)
	python -m pytest -v -m "notebook"

# type-check:
# 	python -m mypy .

conda-env-update:
	$(CONDA) env update $(CONDAFLAGS) -f environment.yml

docker-build:
	docker build -t $(PROJECT) .

docker-run:
	docker run --rm -ti -v $(PWD):/srv $(PROJECT)

template-update:
	pre-commit run --all-files cruft -c .pre-commit-config-weekly.yaml

docs-build:
	cd docs && rm -fr _api && make clean && make html

#integration-tests:
#    python -m pytest -vv --cov=. --cov-report=$(COV_REPORT) tests/integration*.py
#    python -m pytest -vv --doctest-glob='*.md'

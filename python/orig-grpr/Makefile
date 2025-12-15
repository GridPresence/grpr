MODULE := grpr
#UPVERSION := $(shell igor py vnum-plus ${MODULE})
PARALLEL := $(shell nproc)
PYLINT_DEPS := 

.PHONY: test
test:
	python3 -m pytest

.PHONY: lint
lint:
	python3 -m pylint -j ${PARALLEL} src/ ${PYLINT_DEPS}

.PHONY: typehint
typehint:
	python3 -m mypy --ignore-missing-imports --check-untyped-defs src/

.PHONY: format
format:
	python3 -m black src/*/*.py

.PHONY: check
check: format lint typehint test

.PHONY: clean
clean:
	rm -fr dist .mypy_cache .pytest_cache

.PHONY: deploy
deploy: check clean
	tbump --non-interactive --only-patch ${UPVERSION}
	python3 -m build --no-isolation
	python3 -m twine upload -r local dist/* --verbose
	rm -fr dist
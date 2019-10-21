all: help env clean lint test build

.PHONY: all

help:
	@echo "  env         install all production dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  docs        build documentation"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"

env:
	pip install poetry
	poetry install


clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

docs:
	$(MAKE) -C docs html

lint:
	black .


test:
	pytest -s
	#python setup.py test

build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel
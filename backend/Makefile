.PHONY: all clean docs docs-serve lint type test test-cov

CMD:=
PYMODULE:=pyinv_server
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=
SPHINX_ARGS:=docs/ docs/_build -nWE

all: test check lint

lint: 
	$(CMD) flake8 $(PYMODULE) $(TESTS)

check:
	$(MANAGEPY) check

dev:
	$(MANAGEPY) runserver

docs:
	$(CMD) sphinx-build $(SPHINX_ARGS)

docs-serve:
	$(CMD) sphinx-autobuild --port 8001 $(SPHINX_ARGS)

type: 
	$(CMD) mypy $(PYMODULE) $(TESTS) 

test: | $(PYMODULE)
	$(CMD) coverage run --source="$(PYMODULE)" $(PYMODULE)/manage.py test -v 2 $(APPS) $(PYMODULE)
	$(CMD) coverage report

test-cov: test | $(PYMODULE)
	$(CMD) coverage html -d htmlcov

isort:
	$(CMD) isort $(PYMODULE) $(TESTS)

clean:
	git clean -Xdf # Delete all files in .gitignore

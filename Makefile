PY?=/usr/local/var/pyenv/versions/data8/bin/python

BASEDIR=$(CURDIR)

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make notebooks                      build Jupyter notebooks            '
	@echo '   make html                           build html                         '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

notebooks:
	$(PY) $(BASEDIR)/build_notebooks.py

notebooks_local:
	$(PY) $(BASEDIR)/build_notebooks.py --local-home

notebooks_local_force:
	$(PY) $(BASEDIR)/build_notebooks.py --local-home --force

notebooks_local_force_test:
	$(PY) $(BASEDIR)/build_notebooks.py --local-home --force --test 

notebooks_force:
	$(PY) $(BASEDIR)/build_notebooks.py --force

notebooks_test:
	$(PY) $(BASEDIR)/build_notebooks.py --test --force

html:
	$(PY) $(BASEDIR)/build_html.py

html_local:
	$(PY) $(BASEDIR)/build_html.py --home .

html_test:
	$(PY) $(BASEDIR)/build_html.py --test 

html_local_test:
	$(PY) $(BASEDIR)/build_html.py --test --home .

.PHONY: html
PY?=/usr/local/var/pyenv/versions/data8/bin/python

BASEDIR=$(CURDIR)

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make notebooks                      build Jupyter notebooks            '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

notebooks:
	$(PY) $(BASEDIR)/build_notebooks.py

notebooks_force:
	$(PY) $(BASEDIR)/build_notebooks.py --force

notebooks_test:
	$(PY) $(BASEDIR)/build_notebooks.py --test --force
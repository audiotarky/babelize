# -*- coding: utf-8; mode:makefile -*-

PHONY=dev clean

all:
	@echo "nothing to do for all"

dev:
	pip install -r requirements-dev.txt
	python setup.py develop

clean:
	$(RM) $(shell find . -name "*~")

#!/usr/bin/bash

nosetests tests -v -d --with-coverage --cover-package=juxtapy,tests --cover-tests --cover-erase --cover-inclusive --cover-branches

rm .coverage

#!/usr/bin/bash

echo 'Tests' > test_report.txt
echo ' ' >> test_report.txt

nosetests tests -v -d --with-coverage --cover-package=juxtapy,tests --cover-tests --cover-erase --cover-inclusive --cover-branches &> test_report.txt

rm .coverage

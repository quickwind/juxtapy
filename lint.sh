#!/usr/bin/bash

TILDLINE=`printf '~%.s' {1..64}`
HASHLINE=`printf '#%.s' {1..64}`
EQALLINE=`printf '=%.s' {1..64}`

echo "Juxtapy Linting Report" > linting_report.md
echo "======================" >> linting_report.md
date >> linting_report.md
echo "" >> linting_report.md

echo $TILDLINE >> linting_report.md
echo "Report 1: juxtapy lint" >> linting_report.md
echo "----------------------" >> linting_report.md
echo $TILDLINE >> linting_report.md
pylint juxtapy >> linting_report.md

echo "" >> linting_report.md
echo $HASHLINE >> linting_report.md
echo $EQALLINE >> linting_report.md
echo $HASHLINE >> linting_report.md
echo "" >> linting_report.md
echo "" >> linting_report.md

echo $TILDLINE >> linting_report.md
echo "Report 2: tests lint" >> linting_report.md
echo "--------------------" >> linting_report.md
echo $TILDLINE >> linting_report.md
pylint tests >> linting_report.md

echo "project linted"

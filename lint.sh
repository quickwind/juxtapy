#!/usr/bin/bash

# remove trailing whitespace
find . -name "*.py" | xargs sed -i '' -e's/[ ^I]*$//'

# lint project
pylint juxtapy > linting_report.md

echo "project linted"

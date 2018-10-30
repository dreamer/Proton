#!/bin/bash

# This script exists only to easily run pylint on all files in repo.
# You can pass additional pylint parameters to this script, e.g.:
#
# $ ./lint-python.sh --output-format=colorized

run_pylint() {
    git ls-files \
        | xargs file --mime \
        | grep text/x-python \
        | cut -d ':' -f 1 \
        | xargs echo pylint "$@"
}

run_pylint "$@"

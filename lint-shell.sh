#!/bin/bash

# This script exists only to easily run shellcheck on all files in repo.
# You can pass additional shellcheck parameters to this script, e.g.:
#
# $ ./lint-shell.sh --format=json

run_shellcheck() {
    git ls-files \
        | xargs file --mime \
        | grep text/x-shellscript \
        | cut -d ':' -f 1 \
        | xargs shellcheck "$@"
}

run_shellcheck "$@"

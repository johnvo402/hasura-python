#!/usr/bin/env bash

set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT/services/scripts

go test -timeout 2h45m -run "^${NAME}$"

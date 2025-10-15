#!/usr/bin/env bash
set +x
set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT

go test -v -p=1 -tags=integration ./...
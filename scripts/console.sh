#!/bin/bash

set -eo pipefail
ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT

if [ -f "$ROOT/.env" ]; then
  export $(grep -v '^#' "$ROOT/.env" | xargs)
fi
ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT

HASURA_HOST=${HASURA_BASE_URL%"/v1/graphql"}
cd $ROOT/hasura

hasura console --skip-update-check --admin-secret $HASURA_ADMIN_SECRET --endpoint $HASURA_HOST

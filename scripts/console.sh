#!/usr/bin/env bash

set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT

CONTROLLER_HOST=${CONTROLLER_URL%"/v1/graphql"}
cd $ROOT/services/controller

hasura console --skip-update-check --admin-secret $CONTROLLER_ADMIN_SECRET --endpoint $CONTROLLER_HOST

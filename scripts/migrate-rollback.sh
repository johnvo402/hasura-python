#!/bin/bash

set -eo pipefail

DB_DEFAULT=${1:-"database"}
HASURA_HOST=${HASURA_BASE_URL%"/v1/graphql"}
FILE_PATH=$(ls ./hasura/migrations/$DB_DEFAULT | sort -n | tail -n 1)

if [[ -n $2 ]]; then
  VERSION=$2
else
  VERSION=$(echo $FILE_PATH | cut -d'_' -f1)
fi

echo "Rolling back database $DB_DEFAULT to version $VERSION"

hasura migrate apply --version $VERSION --type down --skip-update-check --insecure-skip-tls-verify --database-name $DB_DEFAULT --endpoint $HASURA_HOST --admin-secret $HASURA_ADMIN_SECRET --project ./services/controller

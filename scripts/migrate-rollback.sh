#!/bin/bash

set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT
# Usage:
# ./rollback.sh [VERSION] [DB_NAME]
# Example:
# ./rollback.sh 1700000001 database

VERSION=${1:-""}
DB_DEFAULT="database"

if [[ -z "$VERSION" ]]; then
  echo "❌ Missing migration version!"
  echo "Usage: ./rollback.sh <VERSION> [DATABASE_NAME]"
  exit 1
fi

# Get Hasura base host (strip /v1/graphql from URL)
HASURA_HOST=${HASURA_BASE_URL%"/v1/graphql"}

echo "🔁 Rolling back database '$DB_DEFAULT' to version $VERSION..."

hasura migrate apply \
  --version "$VERSION" \
  --type down \
  --skip-update-check \
  --insecure-skip-tls-verify \
  --database-name "$DB_DEFAULT" \
  --endpoint "$HASURA_HOST" \
  --admin-secret "$HASURA_ADMIN_SECRET" \
  --project ./services/controller

echo "✅ Rollback complete."

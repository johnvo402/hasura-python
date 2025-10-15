#!/bin/bash

set -eo pipefail

# add git hooks for better code lint
# sh -c "$(curl -fsSL https://r.viktoradam.net/githooks)" -- --non-interactive --single

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

CONTROLLER_HOST=${CONTROLLER_URL%"/v1/graphql"}

docker compose exec postgres /bin/bash -c "psql -U postgres -d postgres < /bootstrap/controller.sql"
hasura seed apply --database-name default --endpoint "$CONTROLLER_HOST" --admin-secret $CONTROLLER_ADMIN_SECRET --project ./services/controller
hasura seed apply --database-name notification --endpoint "$CONTROLLER_HOST" --admin-secret $CONTROLLER_ADMIN_SECRET --project ./services/controller
hasura seed apply --database-name geo --endpoint "$CONTROLLER_HOST" --admin-secret $CONTROLLER_ADMIN_SECRET --project ./services/controller
hasura seed apply --database-name ecommerce --endpoint "$CONTROLLER_HOST" --admin-secret $CONTROLLER_ADMIN_SECRET --project ./services/controller
docker compose exec postgres /bin/bash -c "psql -U postgres -d wallet < /bootstrap/wallet.sql"

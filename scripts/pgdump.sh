#!/bin/bash

set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd "$ROOT"

DB="database"
POSTGRES_HOST="${POSTGRES_HOST:-postgres}"  # Default if not set
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-}"
REMOTE_SERVER_USER="${REMOTE_SERVER_USER:-}"
REMOTE_SERVER_IP="${REMOTE_SERVER_IP:-}"
REMOTE_SERVER_PORT="${REMOTE_SERVER_PORT:-22}"

# Ensure required vars are set
require_var() {
  local var_name="$1"
  local var_value="${!var_name}"
  if [[ -z "$var_value" ]]; then
    echo "Error: $var_name is required." >&2
    exit 1
  fi
}

backup() {
  local filepath="$ROOT/.pgdump/$DB.sql"
  mkdir -p "$ROOT/.pgdump"
  rm -f "$filepath"

  require_var POSTGRES_PASSWORD
  require_var POSTGRES_USER

  echo "START backup $DB"
  docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" "$POSTGRES_HOST" pg_dump -U "$POSTGRES_USER" -d "$DB" > "$filepath"
  echo "END backup $DB"
  echo
}

sql() {
  require_var REMOTE_SERVER_USER
  require_var REMOTE_SERVER_IP
  require_var REMOTE_SERVER_PORT

  echo "Fetching .pgdump from remote server..."
  scp -P "$REMOTE_SERVER_PORT" -r \
    "$REMOTE_SERVER_USER@$REMOTE_SERVER_IP:~/hasura-python/.pgdump" .
  echo "Download complete."
}

restore() {
  local filepath="/backup/$DB.sql"

  echo "START restore $DB"
  docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" database sh -c "psql -U $POSTGRES_USER -d $DB < /backup/$POSTGRES.sql"
  echo "END restore $DB"
  echo
}

case "$1" in
  backup)
    backup
    ;;
  sql)
    sql
    ;;
  restore)
    restore
    ;;
  *)
    echo "Usage: $0 {backup|sql|restore}"
    echo "  backup  - Dump database to .pgdump/$DB.sql"
    echo "  sql     - Download .pgdump from remote server"
    echo "  restore - Restore database from /backup/$DB.sql in container"
    exit 1
    ;;
esac
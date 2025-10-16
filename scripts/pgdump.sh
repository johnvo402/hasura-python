#!/bin/bash

set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT
DB_LIST=("default" "cms" "ecommerce" "crm" "geo" "hrm" "notification" "wallet" "project")
POSTGRES_EXEC="docker compose exec postgres"

backup() {
  for db in ${DB_LIST[@]}; do
    local filepath="$ROOT/.pgdump/$db.sql"
    rm -f $filepath
    case "$db" in
    "default")
      DB_NAME="postgres"
      ;;
    *)
      DB_NAME=$db
      ;;
    esac

    echo "START backup $db"
    docker exec -i postgres /bin/bash -c "PGPASSWORD=$POSTGRES_PASSWORD pg_dump --username $POSTGRES_USER $DB_NAME" >$filepath
    #PGPASSWORD=$POSTGRES_PASSWORD pg_dump --host=$BACKUP_HOST --port=$BACKUP_PORT --username=$POSTGRES_USER --dbname=$DB_NAME > $filepath
    echo "END backup $db"
    printf "\n"
  done
}

sql() {
  scp -r -P $REMOTE_SERVER_PORT $REMOTE_SERVER_USER@$REMOTE_SERVER_IP:~/s3-backend/.pgdump .
}

restore() {
  for db in ${DB_LIST[@]}; do
    case "$db" in
    "default")
      DB_NAME="postgres"
      ;;
    *)
      DB_NAME=$db
      ;;
    esac
    echo "START restore $db"
    $POSTGRES_EXEC sh -c "psql -U $POSTGRES_USER -d $DB_NAME < /backup/$db.sql"
    echo "END restore $db"
    printf "\n"
  done
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
*) ;;
esac

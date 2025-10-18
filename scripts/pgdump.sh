#!/bin/bash

set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT
DB="database"
POSTGRES_EXEC="docker compose exec postgres"

backup() {
   local filepath="$ROOT/.pgdump/$DB.sql"
    rm -f $filepath
      DB_NAME=$DB
      ;;
    esac

    echo "START backup $DB"
    docker exec -i postgres /bin/bash -c "PGPASSWORD=$POSTGRES_PASSWORD pg_dump --username $POSTGRES_USER $DB_NAME" >$filepath
    #PGPASSWORD=$POSTGRES_PASSWORD pg_dump --host=$BACKUP_HOST --port=$BACKUP_PORT --username=$POSTGRES_USER --dbname=$DB_NAME > $filepath
    echo "END backup $DB"
    printf "\n"
}

sql() {
  scp -r -P $REMOTE_SERVER_PORT $REMOTE_SERVER_USER@$REMOTE_SERVER_IP:~/s3-backend/.pgdump .
}

restore() {
  DB_NAME=$DB
      ;;
    esac
    echo "START restore $DB"
    $POSTGRES_EXEC sh -c "psql -U $POSTGRES_USER -d $DB_NAME < /backup/$DB.sql"
    echo "END restore $DB"
    printf "\n"
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

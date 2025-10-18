#!/bin/bash

set -eo pipefail

ROOT="$(dirname "${BASH_SOURCE[0]}")/.."
cd $ROOT

http_wait() {
  printf "$1:\t "
  for i in {1..120};
  do
    local code="$(curl -s -o /dev/null -m 2 -w '%{http_code}' $1)"
    if [[ $code != "200" ]]; then
      printf "."
      sleep 1
    else
      printf " OK\n"
      return 0
    fi
  done
  printf "\nERROR$: cannot connect to $1\n"
  exit 1
}

HASURA_HOST=${HASURA_BASE_URL%"/v1/graphql"}

migrate_server() {
  ssh -A "$REMOTE_SERVER_USER@$REMOTE_SERVER_IP" "cd s3-backend
    git checkout $REMOTE_SERVER_BRANH
    git fetch origin && git reset --hard origin/$REMOTE_SERVER_BRANH && git clean -f -d
    make migrate"
}

migrate_local() {
  cd $ROOT/services/controller

  # hasura metadata reload --skip-update-check --admin-secret $HASURA_ADMIN_SECRET --endpoint $HASURA_HOST
  hasura migrate apply --skip-update-check --all-databases --admin-secret $HASURA_ADMIN_SECRET --endpoint $HASURA_HOST
  # hasura metadata reload --skip-update-check --admin-secret $HASURA_ADMIN_SECRET --endpoint $HASURA_HOST
  hasura metadata apply --skip-update-check --admin-secret $HASURA_ADMIN_SECRET --endpoint $HASURA_HOST
}

http_wait "${HASURA_HOST}/healthz"

case "${DEV}" in
  true)
    migrate_server
  ;;
  *)
    migrate_local
  ;;
esac

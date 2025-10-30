.EXPORT_ALL_VARIABLES:

REGISTRY ?= thanhthu
PROJECT ?= hasura-python
VERSION ?= $(shell date +"%Y%m%d")
TAG ?= $(shell git describe --tags --always --dirty)
GIT_COMMIT ?= $(shell git rev-parse HEAD)
GIT_BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD)
ENV_FILE ?= .env
args=$(filter-out $@,$(MAKECMDGOALS))

# export .env file
-include $(ENV_FILE)
export


database:
	docker compose -f docker-compose.yaml -f docker-compose.database.yaml up -d database

dev:
	docker compose -f docker-compose.yaml -f docker-compose.database.yaml -f docker-compose.dev.yaml up -d ${SERVICE}

dev-build:
	docker compose -f docker-compose.yaml -f docker-compose.database.yaml -f docker-compose.dev.yaml up -d --build ${SERVICE}

staging:
	docker compose -f docker-compose.yaml -f docker-compose.database.yaml -f docker-compose.staging.yaml up -d --build ${SERVICE}

clean:
	docker compose -f docker-compose.yaml -f docker-compose.database.yaml -f docker-compose.dev.yaml down --remove-orphans -v


restart:
	docker compose restart $(args)

logs:
	docker-compose logs -f docker-compose.yaml -f docker-compose.dev.yaml $(args)

down:
	docker compose -f docker-compose.yaml -f docker-compose.database.yaml -f docker-compose.dev.yaml down ${SERVICE}

console:
	./scripts/console.sh

generate:
	./scripts/gen-schema.sh

migrate-rollback:
	@bash ./scripts/migrate-rollback.sh ${DB_DEFAULT} ${VERSION}

ssh:
	ssh -p $(REMOTE_SERVER_PORT) $(REMOTE_SERVER_USER)@$(REMOTE_SERVER_IP)

deploy-dev:
	./scripts/deploy.sh ${SERVICE}

migrate:
	./scripts/migrate.sh ${DEV}

.PHONY: pgdump
pgdump:
	./scripts/pgdump.sh $(args)

.PHONY: scripts
scripts:
	./scripts/script.sh ${NAME}

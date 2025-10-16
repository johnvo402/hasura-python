.EXPORT_ALL_VARIABLES:

REGISTRY ?= nexlab
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


postgres:
	docker compose -f docker-compose.yaml -f docker-compose.postgres.yaml up -d postgres

dev:
	docker compose -f docker-compose.yaml -f docker-compose.postgres.yaml -f docker-compose.dev.yaml up -d ${SERVICE}

dev-build:
	docker compose -f docker-compose.yaml -f docker-compose.postgres.yaml -f docker-compose.dev.yaml up -d --build ${SERVICE}

staging:
	docker compose -f docker-compose.yaml -f docker-compose.postgres.yaml -f docker-compose.staging.yaml up -d --build ${SERVICE}

prod:
	docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d --build ${SERVICE}

clean:
	docker compose -f docker-compose.yaml -f docker-compose.postgres.yaml -f docker-compose.dev.yaml down --remove-orphans -v

dev-clean: clean dev-build

restart:
	docker compose restart $(args)

logs:
	docker-compose logs -f docker-compose.yaml -f docker-compose.dev.yaml $(args)

down:
	docker compose -f docker-compose.yaml -f docker-compose.postgres.yaml -f docker-compose.dev.yaml down ${SERVICE}

console:
	./scripts/console.sh

generate:
	./scripts/gen-schema.sh

bootstrap:
	./scripts/bootstrap/bootstrap.sh

migrate-rollback:
	@bash ./scripts/migrate-rollback.sh ${DB_DEFAULT} ${VERSION}

hasura-version:
	@sudo bash ./scripts/hasura-version.sh

quickly-restore:
	@bash ./scripts/quickly-restore.sh

# controller
.PHONY: build-controller
## build-controller: build the controller service
build-controller:
	docker build -t $(REGISTRY)/$(PROJECT)-controller:$(VERSION) services/controller

.PHONY: push-controller
## push-controller: push the controller service to registry
push-controller:
	docker push $(REGISTRY)/$(PROJECT)-controller:$(VERSION)

.PHONY: controller
## controller: build and push the controller service to registry
controller: build-controller push-controller

# auth
.PHONY: build-auth
## build-auth: build the auth service
build-auth:
	docker build -t $(REGISTRY)/$(PROJECT)-auth:$(VERSION) \
		--build-arg TAG=$(TAG) --build-arg GIT_COMMIT=$(GIT_COMMIT) \
		-f services/auth/Dockerfile .

.PHONY: push-auth
## push-auth: push the auth service to registry
push-auth:
	docker push $(REGISTRY)/$(PROJECT)-auth:$(VERSION)

.PHONY: auth
## auth: build and push the auth service to registry
auth: build-auth push-auth

# conversation-api
.PHONY: build-conversation-api
## build-conversation-api: build the conversation-api service
build-conversation-api:
	docker build -t $(REGISTRY)/$(PROJECT)-conversation-api:$(VERSION) \
		--build-arg TAG=$(TAG) --build-arg GIT_COMMIT=$(GIT_COMMIT) \
		-f services/conversation-api/Dockerfile .

.PHONY: push-conversation-api
## push-conversation-api: push the conversation-api service to registry
push-conversation-api:
	docker push $(REGISTRY)/$(PROJECT)-conversation-api:$(VERSION)

.PHONY: conversation-api
## conversation-api: build and push the conversation-api service to registry
conversation-api: build-conversation-api push-conversation-api

# ecommerce-api
.PHONY: build-ecommerce-api
## build-ecommerce-api: build the ecommerce-api service
build-ecommerce-api:
	docker build -t $(REGISTRY)/$(PROJECT)-ecommerce-api:$(VERSION) \
		--build-arg TAG=$(TAG) --build-arg GIT_COMMIT=$(GIT_COMMIT) \
		-f services/ecommerce-api/Dockerfile .

.PHONY: push-ecommerce-api
## push-ecommerce-api: push the ecommerce-api service to registry
push-ecommerce-api:
	docker push $(REGISTRY)/$(PROJECT)-ecommerce-api:$(VERSION)

.PHONY: ecommerce-api
## ecommerce-api: build and push the ecommerce-api service to registry
ecommerce-api: build-ecommerce-api push-ecommerce-api

# export-api
.PHONY: build-export-api
## build-export-api: build the export-api service
build-export-api:
	docker build -t $(REGISTRY)/$(PROJECT)-export-api:$(VERSION) \
		--build-arg TAG=$(TAG) --build-arg GIT_COMMIT=$(GIT_COMMIT) \
		-f services/export-api/Dockerfile .

.PHONY: push-export-api
## push-export-api: push the export-api service to registry
push-export-api:
	docker push $(REGISTRY)/$(PROJECT)-export-api:$(VERSION)

.PHONY: export-api
## export-api: build and push the export-api service to registry
export-api: build-export-api push-export-api

# geo-api
.PHONY: build-geo-api
## build-geo-api: build the geo-api service
build-geo-api:
	docker build -t $(REGISTRY)/$(PROJECT)-geo-api:$(VERSION) \
		--build-arg TAG=$(TAG) --build-arg GIT_COMMIT=$(GIT_COMMIT) \
		-f services/geo-api/Dockerfile .

.PHONY: push-geo-api
## push-geo-api: push the geo-api service to registry
push-geo-api:
	docker push $(REGISTRY)/$(PROJECT)-geo-api:$(VERSION)

.PHONY: geo-api
## geo-api: build and push the geo-api service to registry
geo-api: build-geo-api push-geo-api

.PHONY: run-services
## run-services: start docker services required for integration tests
run-services:
	docker compose -f docker-compose.yaml -f docker-compose.test.yaml up -d postgres controller
	docker compose -f docker-compose.yaml -f docker-compose.test.yaml up controller-migrate

.PHONY: test-integration
## test-integration: run tests that require docker-compose
test-integration: run-services bootstrap
	./scripts/test.sh

.PHONY: go-unit
## go-unit: run go unit tests for all services
go-unit:
	go test ./...

.PHONY: go-fmt
## go-fmt: check formatting of go code
go-fmt:
	./scripts/check_gofmt.sh

GO_MODULES := $(shell find . -not \( -name vendor -prune \) -name go.mod | xargs -n 1 dirname)

.PHONY: go-vet
## go-vet: check go code with go vet
go-vet:
	go vet ./...

.PHONY: go-lint
## go-lint: lint go code
go-lint: go-fmt go-vet

.PHONY: help
## help: prints help message
help:
	@echo "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

# deployment related rules
# ENV can be staging or prod
ALLOWED_ENV = staging prod
ENV ?= prod
K8S_DIR = k8s

ifeq ($(ENV), prod)
	CLOUD_PROJECT = diva-production-383303
	DEFAULT_REPO = asia.gcr.io/$(CLOUD_PROJECT)
	CLUSTER = prod-k8s-cluster
	ZONE = asia-southeast1-b
	KUBECONTEXT = gke_diva-production-383303_asia-southeast1-b_prod-k8s-cluster
endif

.PHONY: validate
## validate: validates for the allowed ENV
validate:
ifeq ($(filter $(ENV),$(ALLOWED_ENV)),)
	$(error unknown env [[ allowed env values - $(ALLOWED_ENV) ]])
endif

# encrypt and decrypt secrets
.PHONY: encrypt-k8s-secrets
encrypt-k8s-secrets:
	gcloud --project $(CLOUD_PROJECT) kms encrypt --location global \
		--keyring $(CLOUD_PROJECT) --key $(CLOUD_PROJECT)-secret \
		--plaintext-file k8s/overlays/prod/secrets.env \
		--ciphertext-file k8s/overlays/prod/secrets.env.encrypted

.PHONY: decrypt-k8s-secrets
decrypt-k8s-secrets:
	gcloud --project $(CLOUD_PROJECT) kms decrypt --location global \
		--keyring $(CLOUD_PROJECT) --key $(CLOUD_PROJECT)-secret \
		--plaintext-file k8s/overlays/prod/secrets.env \
		--ciphertext-file k8s/overlays/prod/secrets.env.encrypted

# encrypt and decrypt secrets
.PHONY: encrypt-k8s-google-cert
encrypt-k8s-google-cert:
	gcloud --project $(CLOUD_PROJECT) kms encrypt --location global \
		--keyring $(CLOUD_PROJECT) --key $(CLOUD_PROJECT)-secret \
		--plaintext-file k8s/overlays/prod/google-cert.json \
		--ciphertext-file k8s/overlays/prod/google-cert.json.encrypted

.PHONY: decrypt-k8s-google-cert
decrypt-k8s-google-cert:
	gcloud --project $(CLOUD_PROJECT) kms decrypt --location global \
		--keyring $(CLOUD_PROJECT) --key $(CLOUD_PROJECT)-secret \
		--plaintext-file k8s/overlays/prod/google-cert.json \
		--ciphertext-file k8s/overlays/prod/google-cert.json.encrypted

.PHONY: encrypt-k8s-onesignal-cert
encrypt-k8s-onesignal-cert:
	gcloud --project $(CLOUD_PROJECT) kms encrypt --location global \
		--keyring $(CLOUD_PROJECT) --key $(CLOUD_PROJECT)-secret \
		--plaintext-file k8s/overlays/prod/onesignal-cert.json \
		--ciphertext-file k8s/overlays/prod/onesignal-cert.json.encrypted

.PHONY: decrypt-k8s-onesignal-cert
decrypt-k8s-onesignal-cert:
	gcloud --project $(CLOUD_PROJECT) kms decrypt --location global \
		--keyring $(CLOUD_PROJECT) --key $(CLOUD_PROJECT)-secret \
		--plaintext-file k8s/overlays/prod/onesignal-cert.json \
		--ciphertext-file k8s/overlays/prod/onesignal-cert.json.encrypted

.PHONY: get-k8s-creds
## get-k8s-creds: Gets the k8s context for the cluster in GCP
get-k8s-creds: validate
	gcloud container clusters get-credentials $(CLUSTER) --zone $(ZONE) --project $(CLOUD_PROJECT)

.PHONY: deploy
deploy: decrypt-k8s-secrets decrypt-k8s-google-cert decrypt-k8s-onesignal-cert
	skaffold run --default-repo $(DEFAULT_REPO) -p $(ENV) \
		--kube-context $(KUBECONTEXT) \
		--label skaffold.dev/run-id="static" \
		--label app.kubernetes.io/managed-by="skaffold"

ssh:
	ssh -p $(REMOTE_SERVER_PORT) $(REMOTE_SERVER_USER)@$(REMOTE_SERVER_IP)

deploy-dev:
	./scripts/deploy.sh ${SERVICE}

migrate:
	./scripts/migrate.sh ${DEV}

.PHONY: pgdump
pgdump:
	./scripts/pgdump.sh $(args)

pgdump-vng-local:
	./scripts/pgdump-vng-local.sh $(args)

.PHONY: pgdump
migrate-container-to-vng:
	./scripts/pgdump-container-vng.sh ${HOST} ${USERNAME} ${PASSWORD}

.PHONY: pgdump
migrate-vng-to-vng:
	./scripts/pgdump-vng-vng.sh ${SOURCE_HOST} ${SOURCE_USERNAME} ${SOURCE_PASSWORD} ${TARGET_HOST} ${TARGET_USERNAME} ${TARGET_PASSWORD}

.PHONY: scripts
scripts:
	./scripts/script.sh ${NAME}

.PHONY: logstash
logstash:
	./scripts/logstash.sh ${CMD}

SHELL=/bin/bash
DIR_NAME ?= $(notdir $(shell pwd))

DOCKER_REGISTRY ?= registry.honestbee.com/
SHORT_NAME ?= ${DIR_NAME}
BUILD_TAG ?= git-$(shell git rev-parse --short HEAD)
IMAGE_PREFIX ?= honestbee

include help.mk
include versioning.mk

## build docker images
build: docker-build

## push docker images
push: docker-push

## install service on a kubernetes cluster
install: kube-apply

## delete service from a kubernetes cluster
delete: kube-delete

## run all containers in stack locally
run: docker-run docker-ports

## get a shell into the built image locally
shell: docker-shell

## list container port mappings
ports: docker-ports

## stop & remove all containers in stack
stop: docker-stop

## follow container logs
logs: docker-logs

## attach terminal to container
attach: docker-attach

docker-build:
	docker build --rm=true --tag=${IMAGE} .
	docker tag ${IMAGE} ${MUTABLE_IMAGE}

docker-logs:
	docker logs -f `docker ps -lqf ancestor=${MUTABLE_IMAGE}`

docker-run: #docker-build
	docker run -d -P --env-file .env --name ${SHORT_NAME} ${MUTABLE_IMAGE}

docker-shell: #docker-build
	docker run -it --rm -v ${PWD}:/usr/src/app --entrypoint /bin/bash ${MUTABLE_IMAGE}

docker-ports:
	@echo "Exposed Ports:"
	@docker inspect --format='{{range $$p, $$conf := .NetworkSettings.Ports}} {{$$p}} -> {{(index $$conf 0).HostPort}} {{end}}' `docker ps -lqf ancestor=${MUTABLE_IMAGE}`

docker-attach:
	@echo "Detach with ^p ^q"
	docker attach `docker ps -lqf ancestor=${MUTABLE_IMAGE}`

docker-stop:
	docker stop ${SHORT_NAME} && docker rm ${SHORT_NAME}

kube-delete:
	-kubectl delete -f manifests/${SHORT_NAME}-bundle.yaml

kube-apply:
	-kubectl apply -f manifests/${SHORT_NAME}-bundle.yaml


SHELL=/bin/bash
DIR_NAME ?= $(notdir $(shell pwd))

DOCKER_REPO ?= mozmeao
SHORT_NAME ?= ${DIR_NAME}
BUILD_TAG ?= git-$(shell git rev-parse --short HEAD)

include help.mk
include versioning.mk

## build docker images
build: docker-build

## push docker images
push: docker-push

## run all containers in stack locally
run: docker-run

## get a shell into the built image locally
shell: docker-shell

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

docker-run:
	docker run -d -P --env-file .env --name ${SHORT_NAME} ${MUTABLE_IMAGE}

docker-shell:
	docker run -it --rm -v ${PWD}:/usr/src/app --env-file .env --entrypoint /bin/sh ${MUTABLE_IMAGE}

docker-attach:
	@echo "Detach with ^p ^q"
	docker attach `docker ps -lqf ancestor=${MUTABLE_IMAGE}`

docker-stop:
	docker stop ${SHORT_NAME} && docker rm ${SHORT_NAME}


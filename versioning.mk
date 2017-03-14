MUTABLE_VERSION ?= latest
VERSION ?= git-$(shell git rev-parse --short HEAD)

IMAGE := ${DOCKER_REPO}/${SHORT_NAME}:${VERSION}
MUTABLE_IMAGE := ${DOCKER_REPO}/${SHORT_NAME}:${MUTABLE_VERSION}

## show image tags
info:
	@echo "Build tag:      ${VERSION}"
	@echo "Repository:     ${DOCKER_REPO}"
	@echo "Immutable tag:  ${IMAGE}"
	@echo "Mutable tag:    ${MUTABLE_IMAGE}"

.PHONY: docker-push
docker-push: docker-mutable-push docker-immutable-push

.PHONY: docker-immutable-push
docker-immutable-push:
	docker push ${IMAGE}

.PHONY: docker-mutable-push
docker-mutable-push:
	docker push ${MUTABLE_IMAGE}


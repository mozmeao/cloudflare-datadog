#!/bin/bash
set -e

DEIS=$1
APP=$2

docker login -e "$DOCKER_EMAIL" -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
docker push ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT}
docker tag -f ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} ${DOCKER_REPOSITORY}:last_successful_build
docker push ${DOCKER_REPOSITORY}:last_successful_build

# Install deis client
curl -sSL http://deis.io/deis-cli/install.sh | sh
./deis login $DEIS --username $DEIS_USERNAME --password $DEIS_PASSWORD
./deis pull ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} -a $APP

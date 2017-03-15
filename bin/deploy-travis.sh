#!/bin/bash
set -e

DEIS=$1
APP=$2

# Install deis client
./bin/deis-cli-install.sh
./deis login $DEIS --username $DEIS_USERNAME --password $DEIS_PASSWORD
./deis pull ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} -a $APP

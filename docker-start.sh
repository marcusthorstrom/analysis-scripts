#!/usr/bin/env bash

# load .env vars
if [ -f .env ]
then
  export $(cat .env | sed 's/^#.*//g' | xargs)
fi

docker start ${DOCKER_COVID_MYSQL}
docker start ${DOCKER_COVID_ADMIN}

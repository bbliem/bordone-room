#!/bin/sh
set -e
GITLAB_TEAM=gruifor
GITLAB_PROJECT=bordone

docker login registry.gitlab.com
docker build -t registry.gitlab.com/${GITLAB_TEAM}/${GITLAB_PROJECT} .
docker push registry.gitlab.com/${GITLAB_TEAM}/${GITLAB_PROJECT}

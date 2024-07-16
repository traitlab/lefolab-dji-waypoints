#!/bin/bash
echo "# -----------------------------------------------------------------------"
echo "script $0"

set -ex

date

# read docker_versions.sh
source docker/docker_versions.sh
echo ${APP_VERSION}
echo ${DOCKER_APP_VERSION}
echo ${DOCKER_VOLUME_VERSION}

/bin/bash git-tag.sh ${APP_VERSION}

/bin/bash git-tag.sh ${DOCKER_APP_VERSION}

date
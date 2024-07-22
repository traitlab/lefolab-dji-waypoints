#!/bin/bash
echo "# -----------------------------------------------------------------------"
echo "script $0"
# used to build the docker; only major.minor version. revision/buildnumber should not appear or new docker image will be build as it's named/tagged with version
APP_VERSION=v0.1.2
DOCKER_APP_VERSION=v0_1
DOCKER_VOLUME_VERSION=v_drone${DOCKER_APP_VERSION}
AUTODEPLOY=true
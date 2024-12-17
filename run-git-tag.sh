#!/bin/bash
echo "# -----------------------------------------------------------------------"
echo "script $0"

set -ex

date

# read docker_versions.sh
source versions.sh
echo ${APP_VERSION}

/bin/bash git-tag.sh ${APP_VERSION}

date
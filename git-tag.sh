#!/bin/bash
echo "# -----------------------------------------------------------------------"
echo "script $0"

set -ex

date

# read docker_versions.sh
source versions.sh
echo ${APP_VERSION}

tag_version=$1

# remove tag local
git tag -d ${tag_version} || true
# remove tag latest local
git tag -d latest || true

# remove tag remote
git push --delete origin ${tag_version} || true
# remove tag latest remote
git push --delete origin latest || true

# create tag
git tag ${tag_version}
# create tag latest
git tag latest

# push tag to remote
git push origin ${tag_version}
git push origin latest

date
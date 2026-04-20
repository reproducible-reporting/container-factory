# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

GPAW_VERSION="25.7.0"
PYTHON_VERSION="3.13"
BUILD_TS="$(date -u +"%Y-%m-%d--%H-%M-%S")"

mkdir -p ../../cache/debian_trixie_amd64_deb
mkdir -p ../../cache/debian_trixie_amd64_lists
mkdir -p ../../cache/root_amd64

CACHE_ARGS="-v ${PWD}/../../cache/debian_trixie_amd64_deb:/var/cache/apt:rw,z \
  -v ${PWD}/../../cache/debian_trixie_amd64_lists:/var/lib/apt/lists:rw,z \
  -v ${PWD}/../../cache/root_amd64:/root/.cache:rw,z"

BUILD_ARGS="--build-arg GPAW_VERSION=${GPAW_VERSION} \
  --build-arg PYTHON_VERSION=${PYTHON_VERSION}"

IMAGE_TAG="tovstra/gpaw-${GPAW_VERSION}:cpu:${BUILD_TS}"

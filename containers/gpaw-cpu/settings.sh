# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

GPAW_VERSION="25.7.0"
PYTHON_VERSION="3.13"
BUILD_ID=$(cat build_id.txt)
../variant.py ${VARIANT} > variant.sh
source variant.sh

mkdir -p ../../cache/debian_trixie_amd64_deb
mkdir -p ../../cache/debian_trixie_amd64_lists
mkdir -p ../../cache/root_amd64

CACHE_ARGS="-v ${PWD}/../../cache/debian_trixie_amd64_deb:/var/cache/apt:rw,z \
  -v ${PWD}/../../cache/debian_trixie_amd64_lists:/var/lib/apt/lists:rw,z \
  -v ${PWD}/../../cache/root_amd64:/root/.cache:rw,z"

BUILD_ARGS="--build-arg GPAW_VERSION=${GPAW_VERSION} \
  --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
  --build-arg GCC_ARCH=${GCC_ARCH}"

IMAGE_TAG="gpaw-${GPAW_VERSION}-cpu:b${BUILD_ID}-${VARIANT}"

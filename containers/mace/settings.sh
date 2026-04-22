# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

set -e

: ${GCC_ARCH:="x86-64-v2"}
: ${CUDA_VERSION:="12"}
PLUMED_VERSION="2.10.0"

mkdir -p cache/root_amd64

PODMAN_RUN_ARGS="-v ${PWD}/cache/root_amd64:/root/.cache:rw,z"

PODMAN_BUILD_ARGS="
  $PODMAN_RUN_ARGS \
  --build-arg NAME=${NAME} \
  --build-arg GCC_ARCH=${GCC_ARCH}
  --build-arg PLUMED_VERSION=${PLUMED_VERSION}
"

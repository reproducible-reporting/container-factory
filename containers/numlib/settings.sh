# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

set -e

: ${GCC_ARCH:="x86-64-v4"}
DEBIAN_VERSION="${VERSION}"
PYTHON_VERSION="3.13"
OPENBLAS_VERSION="0.3.32"
SCALAPACK_VERSION="2.2.0"
FFTW_VERSION="3.3.10"
NUMPY_VERSION="2.4.4"
SCIPY_VERSION="1.17.1"

mkdir -p cache/debian_trixie_amd64_deb
mkdir -p cache/debian_trixie_amd64_lists
mkdir -p cache/root_amd64

PODMAN_RUN_ARGS="
  -v ${PWD}/cache/debian_trixie_amd64_deb:/var/cache/apt:rw,z \
  -v ${PWD}/cache/debian_trixie_amd64_lists:/var/lib/apt/lists:rw,z \
  -v ${PWD}/cache/root_amd64:/root/.cache:rw,z \
"

PODMAN_BUILD_ARGS="
  $PODMAN_RUN_ARGS \
  --build-arg NAME=${NAME} \
  --build-arg GCC_ARCH=${GCC_ARCH} \
  --build-arg DEBIAN_VERSION=${DEBIAN_VERSION} \
  --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
  --build-arg OPENBLAS_VERSION=${OPENBLAS_VERSION} \
  --build-arg SCALAPACK_VERSION=${SCALAPACK_VERSION} \
  --build-arg FFTW_VERSION=${FFTW_VERSION}
  --build-arg NUMPY_VERSION=${NUMPY_VERSION} \
  --build-arg SCIPY_VERSION=${SCIPY_VERSION}
"

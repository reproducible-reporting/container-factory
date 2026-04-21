# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

ARG DEBIAN_VERSION

# ------- STAGE 1: The Base -------

# Use a stripped-down Debian to start
FROM debian:${DEBIAN_VERSION}-slim AS base
ARG PYTHON_VERSION GCC_ARCH

# Set environment variables that persist in the image
ENV UV_NO_MANAGED_PYTHON=1 \
    UV_PYTHON=/usr/bin/python${PYTHON_VERSION} \
    VIRTUAL_ENV=/opt/venv \
    SOURCE_DATE_EPOCH="315532800" \
    PATH="/root/.local/bin:/opt/venv/bin:/opt/bin/:${PATH}" \
    LD_LIBRARY_PATH="/opt/lib:${LD_LIBRARY_PATH}" \
    INCLUDE_PATH="/opt/include:${INCLUDE_PATH}" \
    PKG_CONFIG_PATH="/opt/lib/pkgconfig:${PKG_CONFIG_PATH}" \
    DOWNLOAD_CACHE=/root/.cache/downloads \
    CFLAGS="-O3 -pipe -fPIC -march=${GCC_ARCH}" \
    CXXFLAGS="-O3 -pipe -fPIC -march=${GCC_ARCH}" \
    FFLAGS="-O3 -pipe -fPIC -march=${GCC_ARCH}" \
    FCFLAGS="-O3 -pipe -fPIC -march=${GCC_ARCH}"

# Configure caches and tmp directory
RUN mkdir -p /var/cache/apt /root/.cache/downloads /tmp/build /tmp/dist && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
      > /etc/apt/apt.conf.d/01keep-debs && \
    rm -fv /etc/apt/apt.conf.d/docker-clean

# Install the packages, clean up useless files with impractical permissions for caching
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl python${PYTHON_VERSION} && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Get uv.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a venv
RUN uv venv /opt/venv

# Set the new Python version to help uv find it
ENV UV_PYTHON=/opt/venv/bin/python

# ------- STAGE 2: The Builder -------

FROM base AS builder
ARG NAME

# Copy some static files
COPY containers/${NAME}/static/debian-packages-builder.txt /tmp/debian-packages-builder.txt
COPY static/download.sh /tmp/download.sh

# Install the packages
RUN apt-get install -y --no-install-recommends $(grep -v '^#' /tmp/debian-packages-builder.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Download OpenBLAS
ARG OPENBLAS_VERSION
RUN /tmp/download.sh https://github.com/OpenMathLib/OpenBLAS/releases/download/v${OPENBLAS_VERSION}/OpenBLAS-${OPENBLAS_VERSION}.tar.gz

# Unpack, build and install OpenBLAS
RUN tar -xzf /root/.cache/downloads/OpenBLAS-${OPENBLAS_VERSION}.tar.gz -C /tmp/build && \
    cd /tmp/build/OpenBLAS-${OPENBLAS_VERSION} && \
    make \
     DYNAMIC_ARCH=1 \
     TARGET=GENERIC \
     NUM_THREADS=256 \
     USE_OPENMP=1 \
     CROSS=1 \
     -j$(nproc) && \
    make PREFIX=/opt install

# Download ScaLAPACK
ARG SCALAPACK_VERSION
RUN /tmp/download.sh https://github.com/Reference-ScaLAPACK/scalapack/archive/refs/tags/v${SCALAPACK_VERSION}.tar.gz ScaLAPACK-${SCALAPACK_VERSION}.tar.gz

# Unpack, build and install ScaLAPACK
RUN tar -xzf /root/.cache/downloads/ScaLAPACK-${SCALAPACK_VERSION}.tar.gz -C /tmp/build && \
    cd /tmp/build/scalapack-${SCALAPACK_VERSION} && \
    mkdir build && \
    cd build && \
    cmake .. \
     -DCMAKE_BUILD_TYPE=Release \
     -DCMAKE_C_COMPILER=mpicc \
     -DCMAKE_Fortran_COMPILER=mpif90 \
     -DCMAKE_C_FLAGS="${CFLAGS} -Wno-error=implicit-function-declaration -O2" \
     -DCMAKE_Fortran_FLAGS="${FFLAGS} -fallow-argument-mismatch -O2" \
     -DBUILD_SHARED_LIBS=ON \
     -DBLAS_LIBRARIES="/opt/lib/libopenblas.so" \
     -DLAPACK_LIBRARIES="/opt/lib/libopenblas.so" \
     -DCMAKE_PREFIX_PATH=/opt \
     -DCMAKE_INSTALL_PREFIX=/opt && \
    make -j$(nproc) && \
    make install

# Download FFTW
ARG FFTW_VERSION
RUN /tmp/download.sh http://www.fftw.org/fftw-${FFTW_VERSION}.tar.gz

# Unpack, build and install FFTW
RUN tar -xzf /root/.cache/downloads/fftw-${FFTW_VERSION}.tar.gz -C /tmp/build && \
    cd /tmp/build/fftw-${FFTW_VERSION} && \
    ./configure \
      --prefix=/opt \
      --enable-shared \
      --enable-openmp \
      --enable-mpi \
      --enable-sse2 \
      --enable-avx \
      --enable-avx2 \
      --enable-avx512 \
      --enable-avx-128-fma && \
    make -j$(nproc) && \
    make install

# Download NumPy
ARG NUMPY_VERSION
RUN /tmp/download.sh https://files.pythonhosted.org/packages/source/n/numpy/numpy-${NUMPY_VERSION}.tar.gz

# Unpack, build and install NumPy
RUN tar -xzf /root/.cache/downloads/numpy-${NUMPY_VERSION}.tar.gz -C /tmp/build && \
    cd /tmp/build/numpy-${NUMPY_VERSION} && \
    uv pip install meson-python==0.19.0 cython==3.2.4 && \
    uv build --wheel . \
      --no-build-isolation && \
    mkdir -p /tmp/dist && \
    cp dist/*.whl /tmp/dist/

# Download SciPy
ARG SCIPY_VERSION
RUN /tmp/download.sh https://files.pythonhosted.org/packages/source/s/scipy/scipy-${SCIPY_VERSION}.tar.gz

# Unpack, build and install SciPy (using a NumPy from PyPI)
RUN tar -xzf /root/.cache/downloads/scipy-${SCIPY_VERSION}.tar.gz -C /tmp/build && \
    cd /tmp/build/scipy-${SCIPY_VERSION} && \
    uv pip install pythran==0.18.1 pybind11==3.0.4 tempita==0.6.0 numpy==${NUMPY_VERSION} && \
    uv build --wheel . --no-build-isolation && \
    cp dist/*.whl /tmp/dist/

# ------- STAGE 3: The Runner -------

FROM base AS runner
ARG NAME
LABEL org.opencontainers.image.source="https://github.com/reproducible-reporting/container-factory" \
      org.opencontainers.image.title=${NAME} \
      org.opencontainers.image.description="Base image with numerical libraries"

# Copy the build requirements file
COPY containers/${NAME}/static/debian-packages-runner.txt /tmp/debian-packages-runner.txt

# Install the packages
RUN apt-get install -y --no-install-recommends $(grep -v '^#' /tmp/debian-packages-runner.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Copy the compiled binaries, libraries and include files from the builder stage
COPY --from=builder /opt/venv/ /opt/venv/
COPY --from=builder /opt/bin/ /opt/bin/
COPY --from=builder /opt/include/ /opt/include/
COPY --from=builder /opt/lib/ /opt/lib/

# Copy the wheels and install them with uv
COPY --from=builder /tmp/dist/ /tmp/dist/
RUN uv pip install /tmp/dist/*.whl

# ------- STAGE 4: The Tester -------

FROM runner AS tester

RUN uv -V

RUN python --version

RUN ldd /opt/lib/libopenblas.so

RUN ldd /opt/lib/libscalapack.so

RUN ldd /opt/lib/libfftw3.so

RUN ldd /opt/venv/lib/python3.*/site-packages/numpy/_core/_multiarray_umath.cpython-*.so && \
    python -c "import numpy; print(numpy.__version__)"

RUN ldd /opt/venv/lib/python3.*/site-packages/scipy/linalg/_fblas.cpython-*.so && \
    python -c "import scipy; print(scipy.__version__)"

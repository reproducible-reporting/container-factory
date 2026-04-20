# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

ARG GPAW_VERSION
ARG PYTHON_VERSION
ARG GCC_ARCH

# ------- STAGE 1: The Base -------

# Use a stripped-down Debian to start
FROM debian:13.4-slim AS base
ARG PYTHON_VERSION

# Set environment variables that persist in the image
ENV UV_NO_MANAGED_PYTHON=1 \
    UV_PYTHON=/usr/bin/python${PYTHON_VERSION} \
    VIRTUAL_ENV=/opt/venv \
    PATH="/root/.local/bin:/opt/venv/bin:$PATH"

# Configure caches and create mount points
RUN mkdir -p /var/cache/apt /root/.cache && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
      > /etc/apt/apt.conf.d/01keep-debs && \
    rm -fv /etc/apt/apt.conf.d/docker-clean

# Install the packages, clean up useless files with impractical permissions for cachging
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
ARG GPAW_VERSION
ARG GCC_ARCH

# Copy the build requirements file
COPY debian-packages-builder.txt /debian-packages-builder.txt

# Install the packages
RUN apt-get install -y --no-install-recommends $(grep -v '^#' /debian-packages-builder.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

RUN mkdir -p /root/.cache/downloads && \
    DEST=/root/.cache/downloads/gpaw-${GPAW_VERSION}.tar.gz && \
    if [ ! -s "$DEST" ]; then \
      curl -vfL \
        "https://pypi.io/packages/source/g/gpaw/gpaw-${GPAW_VERSION}.tar.gz" \
        -o "$DEST.tmp" && \
      mv "$DEST.tmp" "$DEST"; \
    fi && \
    mkdir -p /tmp/build && \
    tar -xzf "$DEST" -C /tmp/build

RUN echo "VIRTUAL_ENV=$VIRTUAL_ENV" && ls /opt/venv/bin/

# Build and install the GPAW wheel
COPY siteconfig.py /tmp/build/gpaw-${GPAW_VERSION}/siteconfig.py
RUN export CFLAGS="-O3 -pipe -march=${GCC_ARCH}" && \
    export CXXFLAGS="${CFLAGS}" && \
    export FFLAGS="${CFLAGS}" && \
    export FCFLAGS="${FFLAGS}" && \
    uv pip install wheel==0.46.3 numpy==2.4.4 setuptools==82.0.1 ase==3.28.0 && \
    cd /tmp/build/gpaw-${GPAW_VERSION} && \
    uv build --wheel --out-dir ./dist --no-build-isolation && \
    cp -a dist /root/

# ------- STAGE 3: The Runner -------

FROM base AS runner
ARG GPAW_VERSION
ARG CPU_ARCH_TIER
LABEL org.opencontainers.image.source="https://github.com/reproducible-reporting/container-factory" \
      org.opencontainers.image.title="gpaw-cpu" \
    org.opencontainers.image.description="GPAW ${GPAW_VERSION} CPU runtime image (${CPU_ARCH_TIER})"

# Copy the run requirements file
COPY debian-packages-runner.txt /debian-packages-runner.txt

# Install the packages
RUN apt-get install -y --no-install-recommends $(grep -v '^#' /debian-packages-runner.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Copy the built wheel from the builder stage
COPY --from=builder /root/dist/ /root/dist/

# Show wheel file
RUN ls -l /root/dist/*.whl

# Install the GPAW wheel
RUN uv pip install numpy==2.4.4 ase==3.28.0 /root/dist/*.whl

# ------- STAGE 4: Testing -------

FROM runner AS tester

RUN ldd /opt/venv/lib/python3.13/site-packages/_gpaw.cpython-313-x86_64-linux-gnu.so

RUN gpaw test

RUN mpiexec -n 2 --allow-run-as-root gpaw test

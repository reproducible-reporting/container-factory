# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

ARG GCC_ARCH

# ------- STAGE 1: The Builder -------

FROM localhost/numlib:v13.4-b1-${GCC_ARCH} AS builder
ARG NAME

# Copy the build requirements file
COPY containers/${NAME}/static/debian-packages-builder.txt /tmp/debian-packages-builder.txt
COPY static/download.sh /tmp/download.sh

# Install the packages
RUN apt-get install -y --no-install-recommends $(grep -v '^#' /tmp/debian-packages-builder.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Download LibXC
ARG LIBXC_VERSION
RUN /tmp/download.sh "https://gitlab.com/libxc/libxc/-/archive/${LIBXC_VERSION}/libxc-${LIBXC_VERSION}.tar.bz2"

# Build and install LibXC
RUN tar -xjf /root/.cache/downloads/libxc-${LIBXC_VERSION}.tar.bz2 -C /tmp/build && \
    cd /tmp/build/libxc-${LIBXC_VERSION} && \
    ([ -f configure ] || autoreconf -i) && \
    ./configure --prefix=/opt --enable-shared --disable-static --disable-fortran && \
    make -j && \
    make install

# Download the GPAW source code
ARG GPAW_VERSION
RUN /tmp/download.sh "https://pypi.io/packages/source/g/gpaw/gpaw-${GPAW_VERSION}.tar.gz"

# Build and install the GPAW wheel
COPY containers/${NAME}/static/siteconfig.py /tmp/build/gpaw-${GPAW_VERSION}/siteconfig.py
RUN tar -xzf /root/.cache/downloads/gpaw-${GPAW_VERSION}.tar.gz -C /tmp/build && \
    cd /tmp/build/gpaw-${GPAW_VERSION} && \
    uv pip install --reinstall numpy==2.4.4 && \
    uv pip install wheel==0.46.3 setuptools==82.0.1 ase==3.28.0 && \
    uv build --wheel --out-dir /tmp/dist --no-build-isolation

# ------- STAGE 2: The Runner -------

FROM localhost/numlib:v13.4-b1-${GCC_ARCH} AS runner
ARG NAME GPAW_VERSION
LABEL org.opencontainers.image.source="https://github.com/reproducible-reporting/container-factory" \
      org.opencontainers.image.title=${NAME} \
      org.opencontainers.image.description="GPAW ${GPAW_VERSION} CPU runtime image (${GCC_ARCH})"

# Copy the run requirements file
COPY containers/${NAME}/static/debian-packages-runner.txt /debian-packages-runner.txt

# Install the packages
RUN apt-get install -y --no-install-recommends $(grep -v '^#' /debian-packages-runner.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Copy the build artifacts
COPY --from=builder /tmp/dist/ /tmp/dist/
COPY --from=builder /opt/include/ /opt/include/
COPY --from=builder /opt/lib/ /opt/lib/

# Show wheel file
RUN ls -l /tmp/dist/*.whl

# Install the GPAW wheel
RUN uv pip install numpy==2.4.4 ase==3.28.0 /tmp/dist/*.whl

# ------- STAGE 3: Testing -------

FROM runner AS tester

RUN ldd /opt/venv/lib/python3.13/site-packages/_gpaw.cpython-313-x86_64-linux-gnu.so

RUN gpaw test

RUN mpiexec -n 2 --allow-run-as-root gpaw test

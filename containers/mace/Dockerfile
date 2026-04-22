# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

ARG GCC_ARCH

# ------- STAGE 1: The Builder -------

FROM localhost/numlib:v13.4-b1-${GCC_ARCH} AS builder
ARG NAME

# Install the packages
COPY containers/${NAME}/static/debian-packages-builder.txt /tmp/debian-packages-builder.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends $(grep -v '^#' /tmp/debian-packages-builder.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Download the Plumed source code
ARG PLUMED_VERSION
COPY static/download.sh /tmp/download.sh
RUN /tmp/download.sh "https://files.pythonhosted.org/packages/source/p/plumed/plumed-${PLUMED_VERSION}.tar.gz" plumed-${PLUMED_VERSION}.tar.gz

# Build the Plumed wheel
RUN tar -xzf /root/.cache/downloads/plumed-${PLUMED_VERSION}.tar.gz -C /tmp/build && \
    cd /tmp/build/plumed-${PLUMED_VERSION} && \
    uv build . --wheel --out-dir /tmp/dist --no-build-isolation

# ------- STAGE 2: The Runner -------

FROM localhost/numlib:v13.4-b1-${GCC_ARCH} AS runner
ARG NAME
LABEL org.opencontainers.image.source="https://github.com/reproducible-reporting/container-factory" \
      org.opencontainers.image.title=${NAME} \
      org.opencontainers.image.description="MACE"

# Install the packages
COPY containers/${NAME}/static/debian-packages-runner.txt /debian-packages-runner.txt
RUN apt-get install -y --no-install-recommends $(grep -v '^#' /debian-packages-runner.txt) && \
    rm -rf /var/lib/apt/lists/partial /var/lib/apt/lists/auxfiles /var/cache/apt/archives/partial

# Copy the wheel from the builder stage

# Install MACE with the Plumed wheel
COPY --from=builder /tmp/dist/ /tmp/dist/
COPY containers/${NAME}/static/requirements.txt /tmp/requirements.txt
COPY containers/${NAME}/static/constraints.txt /tmp/constraints.txt
RUN cd /tmp && uv pip install /tmp/dist/*.whl -r requirements.txt --constraint constraints.txt

# ------- STAGE 3: Testing -------

FROM runner AS tester

RUN python -c "import mace; print(mace.__version__)"

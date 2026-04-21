# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

ARG GCC_ARCH

# ------- STAGE 1: The Runner -------

FROM localhost/numlib:v13.4-b1-${GCC_ARCH} AS runner
ARG NAME MACE_VERSION CUDA_VERSION ASE_VERSION
LABEL org.opencontainers.image.source="https://github.com/reproducible-reporting/container-factory" \
      org.opencontainers.image.title=${NAME} \
    org.opencontainers.image.description="MACE ${MACE_VERSION} (CUDA ${CUDA_VERSION}, ASE ${ASE_VERSION})"

# Install MACE
RUN uv pip install mace_torch[wandb,cueq-cuda-${CUDA_VERSION}]==${MACE_VERSION} ase==${ASE_VERSION}

# ------- STAGE 2: Testing -------

FROM runner AS tester

RUN python -c "import mace; print(mace.__version__)"

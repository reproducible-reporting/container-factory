# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

ARG GCC_ARCH

# ------- STAGE 1: The Runner -------

FROM localhost/numlib:v13.4-b1-${GCC_ARCH} AS runner
ARG NAME
LABEL org.opencontainers.image.source="https://github.com/reproducible-reporting/container-factory" \
      org.opencontainers.image.title=${NAME} \
      org.opencontainers.image.description="MACE"

# Install MACE
COPY containers/${NAME}/static/pyproject.toml /tmp/pyproject.toml
RUN cd tmp && \
  uv pip install .

# ------- STAGE 2: Testing -------

FROM runner AS tester

RUN python -c "import mace; print(mace.__version__)"

#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

source settings.sh
podman build \
  ${CACHE_ARGS} \
  ${BUILD_ARGS} \
  --target runner \
  -t ${IMAGE_TAG} .

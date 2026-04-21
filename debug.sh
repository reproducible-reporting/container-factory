#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

# Get into a container with a given ID and start a bash session.
#
# Usage:
#
#   debug.sh <container_id>

ID=${1}
NAME=${2}
if [ -z "${ID}" ] || [ -z "${NAME}" ]; then
  echo "Usage: debug.sh <container_id> <container_name>"
  exit 1
fi

source containers/${NAME}/settings.sh
podman run -it ${PODMAN_RUN_ARGS} ${ID} bash

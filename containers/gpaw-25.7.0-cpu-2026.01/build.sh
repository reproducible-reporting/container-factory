#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

mkdir -p ../../cache/debian_trixie_amd64_deb
mkdir -p ../../cache/debian_trixie_amd64_lists
mkdir -p ../../cache/root_amd64
podman build \
  -v ${PWD}/../../cache/debian_trixie_amd64_deb:/var/cache/apt:rw,z \
  -v ${PWD}/../../cache/debian_trixie_amd64_lists:/var/lib/apt/lists:rw,z \
  -v ${PWD}/../../cache/root_amd64:/root/.cache:rw,z \
  --target runner \
  -t tovstra/gpaw-25.7.0-cpu-2026.01 .

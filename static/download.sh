#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

# Helper script to download source tarballs to the local cache

URL="${1}"
if [ -z "${URL}" ]; then
  echo "Usage: $0 <url> [filename]"
  exit 1
fi
FILENAME="${2}"
if [ -z "${FILENAME}" ]; then
  FILENAME="$(basename "${URL}")"
fi
DESTINATION="${DOWNLOAD_CACHE}/${FILENAME}"
if [ -f "${DESTINATION}" ]; then
  echo "File ${DESTINATION} already exists, skipping download"
  exit 0
else
  echo "Downloading ${URL} to ${DESTINATION}"
  curl -L -o "${DESTINATION}" "${URL}"
fi

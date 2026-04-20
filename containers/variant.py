#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0
"""Load environment variables for a container variant."""

import argparse
import json
import sys

parser = argparse.ArgumentParser(description="Load environment variables for a container variant.")
parser.add_argument("variant", help="The variant to load settings for.", default=None, nargs="?")
args = parser.parse_args()

with open("variants.json") as f:
    variants = json.load(f)
if args.variant is None:
    print("Error: No variant specified. Available variants: " + ", ".join(variants.keys()), file=sys.stderr)
    exit(1)
if args.variant not in variants:
    print(f"Error: variant '{args.variant}' not found in variants.json.", file=sys.stderr)
    print(f"Available variants: {', '.join(variants.keys())}", file=sys.stderr)
    exit(1)
for key, value in variants[args.variant].items():
    print(f"export {key}=\"{value}\"")

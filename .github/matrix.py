#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0
"""Construct a build matrix with containers and their settings.

Test as follows from the root of the repo:

.github/matrix.py << EOF
containers/gpaw-cpu/settings.sh
containers/gpaw-gpu/build_id.txt
containers/random-file.txt
EOF

.github/matrix.py << EOF
.github/matrix.py
EOF
"""

import json
import sys
from pathlib import Path

changed_containers = set()

build_all = False
for line in sys.stdin:
    line = line.strip()
    if line.startswith("containers/"):
        changed_containers.add(line.split("/")[1])
    elif line in [".github/matrix.py", ".github/workflows/build.yaml"]:
        build_all = True
        break

if build_all:
    for path in Path("containers").glob("*/build.sh"):
        changed_containers.add(path.parent.name)

include = []
for container in changed_containers:
    if not Path(f"containers/{container}/build.sh").is_file():
        continue
    path_matrix = Path(f"containers/{container}/variants.json")
    if path_matrix.is_file():
        first = True
        with open(path_matrix) as f:
            for key in json.load(f).keys():
                include.append({"container": container, "variant": key, "test": first})
                first = False
    else:
        include.append({"container": container, "variant": "default", "test": True})
print("include=" + json.dumps(include))

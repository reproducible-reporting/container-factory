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
"""

import json
import sys
from pathlib import Path

changed_containers = set(line.split("/")[1] for line in sys.stdin if line.startswith("containers/"))
include = []
for container in changed_containers:
    if not Path(f"containers/{container}/build.sh").is_file():
        continue
    path_matrix = Path(f"containers/{container}/variants.json")
    if path_matrix.is_file():
        with open(path_matrix) as f:
            for key in json.load(f).keys():
                include.append({"container": container, "variant": key})
    else:
        include.append({"container": container, "variant": "default"})
print("include=" + json.dumps(include))

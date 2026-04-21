#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

import json
from string import Template

from stepup.core.api import runsh, static, glob, amend, mkdir, pool, getenv
from stepup.core.utils import string_to_bool
from path import Path


BUILD_SH = """\
source containers/${NAME}/settings.sh
podman build ${PODMAN_BUILD_ARGS} --target runner -t ${IMAGE} -f containers/${NAME}/Dockerfile .
"""

TEST_SH = """\
source containers/${NAME}/settings.sh
podman build ${PODMAN_BUILD_ARGS} --target tester -f containers/${NAME}/Dockerfile .
"""

DEBUG_SH = """\
ID=${1}
if [ -z "$ID" ]; then
    echo "Usage: $0 <container_id>"
    exit 1
fi
source containers/${NAME}/settings.sh
podman run ${PODMAN_RUN_ARGS} -it ${ID} bash
"""

PUSH_SH = """\
source containers/${NAME}/settings.sh
podman tag ${IMAGE} docker.io/tovrstra/${IMAGE}
podman push docker.io/tovrstra/${IMAGE}
"""

SCRIPTS = {
    "build": BUILD_SH,
    "test": TEST_SH,
    "debug": DEBUG_SH,
    "push": PUSH_SH,
}


def write_script(template_str: str, env: dict[str, str], path: Path) -> None:
    amend(out=path)
    with open(path, "w") as fh:
        print("#!/usr/bin/env bash", file=fh)
        for key, value in env.items():
            print(f"{key}=\"{value}\"", file=fh)
        print(template_str, file=fh)
    path.chmod(0o755)


def parse_dockerfile(path: Path, env: dict[str, str]) -> set[str]:
    amend(inp=path)
    inp = set()
    with open(path) as fh:
        for line in fh:
            if line.startswith("FROM "):
                image = line.split()[1]
                if image.startswith("localhost/"):
                    image = Template(image).substitute(env)
                    name, tag = image[len("localhost/"):].split(":")
                    inp.add(f"containers/{name}/output/build-{tag}.log")
            elif line.startswith("COPY "):
                src = line.split()[1]
                if not src.startswith("--from="):
                    src = Template(src).substitute(env)
                    inp.add(src)
    return inp


do_push = string_to_bool(getenv("DO_PUSH", "false"))
pool("cache", 1)
glob("static/**")
static("containers/")
for container in glob("containers/*/"):
    name = container.parent.name
    if glob(container / "Dockerfile"):
        # Expected files
        static(container / "config.json", container / "settings.sh")
        glob(container / "static/**")
        container_inp = [container / "Dockerfile", container / "config.json", container / "settings.sh"]

        # Load config
        amend(inp=container / "config.json")
        with open(container / "config.json") as fh:
            config = json.load(fh)
        version = config["version"]
        build_id = config["build_id"]
        variants = config.get("variants", {None: {}})

        amend(out=container / "output/")
        Path(container / "output/").mkdir_p()
        first = True
        for variant, env in variants.items():
            # Prepare env
            tag = f"v{version}-b{build_id}"
            if variant is not None:
                tag += f"-{variant}"
            image = f"{name}:{tag}"
            env["NAME"] = name
            env["VERSION"] = version
            env["BUILD_ID"] = str(build_id)
            env["TAG"] = tag
            env["IMAGE"] = image

            # Determine local dependencies of the Dockerfile
            variant_inp = list(container_inp)
            variant_inp.extend(parse_dockerfile(container / "Dockerfile", env))

            # Write debug script
            path_script = container / f"output/debug-{tag}.sh"
            write_script(SCRIPTS["debug"], env, path_script)

            # Build and test
            targets = ["build", "test"] if first else ["build"]
            if do_push:
                targets.append("push")
            for target in targets:
                path_script = container / f"output/{target}-{tag}.sh"
                write_script(SCRIPTS[target], env, path_script)
                path_log = container / f"output/{target}-{tag}.log"
                runsh(
                    f"./{path_script} > {path_log} 2>&1",
                    inp=[path_script, *variant_inp],
                    out=path_log,
                    pool="cache",
                )
                variant_inp.append(path_log)

            first = False

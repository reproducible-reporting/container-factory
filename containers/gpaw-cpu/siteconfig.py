# SPDX-FileCopyrightText: © 2026 Toon Verstraelen <Toon.Verstraelen@UGent.be>
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa
fftw = True
scalapack = True
libraries += ["fftw3", "openblas", "xc", "scalapack-openmpi"]

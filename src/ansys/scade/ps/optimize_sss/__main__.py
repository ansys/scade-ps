# -*- coding: utf-8 -*-

# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Ansys SCADE Power Scripts: Optimize sss scenarios."""

import argparse

from ansys.scade.apitools import declare_project

# isort: split
# must be imported after ansys.scade.apitools
from ansys.scade.ps.optimize_sss.sssopt import main as optimize_sss_main

tool = 'Ansys SCADE Power Scripts: Optimize test scenarios (SSS)'


def main():
    """Implement ``ansys.scade.ps.optimize_sss.__main__:main`` packages's script."""
    parser = argparse.ArgumentParser(description=tool)

    parser.add_argument('-m', '--model', metavar='<model>', help='Scade model', required=True)
    parser.add_argument('-a', '--alias', metavar='<alias>', help='alias file (sss)', required=True)
    parser.add_argument(
        '-s', '--scenario', metavar='<scenario>', help='input scenario (sss)', required=True
    )
    parser.add_argument(
        '-o', '--output', metavar='<output>', help='output scenario (csv)', required=True
    )

    options = parser.parse_args()

    assert declare_project  # nosec B101  # declare_project must be defined on Windows
    declare_project(options.model)

    code = optimize_sss_main(options.scenario, options.alias, options.output)
    exit(code)


if __name__ == '__main__':
    # run with python.exe -m ansys.scade.ps.optimize_sss
    main()
# else:  # run with ansys_scade_ps_optimize_sss.exe

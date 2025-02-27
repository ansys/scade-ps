# -*- coding: utf-8 -*-

# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
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

"""Ansys SCADE Power Scripts: Create default notes for Scade models."""

import argparse

from ansys.scade.apitools import declare_project

# isort: split
# must be imported after ansys.scade.apitools
from .default_notes import main as default_notes_main, tool


def main():
    """Implement ``ansys.scade.ps.default_notes.__main__:main`` packages's script."""
    parser = argparse.ArgumentParser(description=tool)
    parser.add_argument(
        '-p', '--projects', metavar='<projects>', help='SCADE Suite projects', nargs='+'
    )
    options = parser.parse_args()

    assert declare_project
    for project in options.projects:
        declare_project(project)
    code = default_notes_main()
    exit(code)


if __name__ == '__main__':
    # run with python.exe -m ansys.scade.ps.default_notes
    main()

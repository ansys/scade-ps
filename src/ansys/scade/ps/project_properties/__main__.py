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

"""Ansys SCADE Power Scripts: Access to SCADE project properties."""

import argparse
from pathlib import Path

from ansys.scade.apitools import declare_project

# isort: split
# must be imported after ansys.scade.apitools
from ansys.scade.ps.project_properties.copy_properties import main as copy_properties_main
from ansys.scade.ps.project_properties.create_template import main as create_template_main

tool = 'Ansys SCADE Power Scripts: Access to SCADE project properties'


def main():
    """Implement ``ansys.scade.ps.project_properties.__main__:main`` packages's script."""
    parser = argparse.ArgumentParser(description=tool)
    parser.add_argument(
        '-p', '--project', metavar='<project>', help='SCADE Suite project', required=True
    )
    subparsers = parser.add_subparsers(help='project properties sub-commands')

    # schema
    template_parser = subparsers.add_parser('template', help='Create a schema template')
    template_parser.add_argument(
        '-o', '--output', metavar='<template file>', help='output template file', required=True
    )
    template_parser.set_defaults(cmd='template')

    # copy
    copy_parser = subparsers.add_parser('copy', help='Copy tool properties')
    copy_parser.add_argument(
        '-s', '--schema', metavar='<schema>', help='input schema file (JSON)', required=True
    )
    copy_parser.add_argument(
        '-p',
        '--projects',
        metavar='<project>',
        help='project files to update (ETP)',
        nargs='+',
        required=True,
    )
    copy_parser.set_defaults(cmd='copy')

    options = parser.parse_args()
    assert declare_project
    declare_project(options.project)
    if options.cmd == 'template':
        code = create_template_main(options.output)
    else:
        assert options.cmd == 'copy'
        for project in options.projects:
            declare_project(project)
        code = copy_properties_main(Path(options.project).name, options.schema)
    exit(code)


if __name__ == '__main__':
    # run with python.exe -m ansys.scade.ps.project_properties
    main()
# else:  # run with ansys_scade_ps_project_properties.exe

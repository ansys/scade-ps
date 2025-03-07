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

"""Ansys SCADE Power Scripts: Change duplicate oids."""

import argparse

from ansys.scade.apitools import declare_project

# isort: split
# must be imported after ansys.scade.apitools
from ansys.scade.ps.change_oids.find_duplicates import main as find_duplicates_main
from ansys.scade.ps.change_oids.new_oids import main as new_oids_main

tool = 'Ansys SCADE Power Scripts: Change duplicate OIDs'


def main():
    """Implement ``ansys.scade.ps.change_oids.__main__:main`` packages's script."""
    parser = argparse.ArgumentParser(description=tool)
    subparsers = parser.add_subparsers(help='change_oids sub-commands')

    # find
    find_parser = subparsers.add_parser('find', help='Find duplicate OIDs')
    find_parser.add_argument(
        '-p',
        '--projects',
        metavar='<project>',
        help='SCADE Suite projects',
        required=True,
        nargs='+',
    )
    find_parser.add_argument(
        '-x',
        '--extension',
        metavar='<extension>',
        help='result file extension',
        default='.dupoids.txt',
    )
    find_parser.add_argument(
        '-d', '--dump_paths', help='print model element paths', action='store_true'
    )
    find_parser.set_defaults(cmd='find')

    # change
    change_parser = subparsers.add_parser('new', help='Create new OIDs')
    change_parser.add_argument(
        '-p', '--project', metavar='<project>', help='SCADE Suite project', required=True
    )
    change_parser.add_argument(
        '-f', '--file', metavar='<input file>', help='input file', required=True
    )
    change_parser.add_argument(
        '-m', '--map', metavar='<output map file>', help='output map file', required=True
    )
    change_parser.add_argument('-l', '--log', metavar='<log file>', help='log file', default='')
    change_parser.set_defaults(cmd='change')

    options = parser.parse_args()

    assert declare_project
    if options.cmd == 'find':
        for project in options.projects:
            declare_project(project)
        code = find_duplicates_main(options.extension, options.dump_paths)
    else:
        assert options.cmd == 'change'
        declare_project(options.project)
        code = new_oids_main(options.file, options.map, options.log)
    exit(code)


if __name__ == '__main__':
    # run with python.exe -m ansys.scade.ps.change_oids
    main()
# else:  # run with ansys_scade_ps_change_oids.exe

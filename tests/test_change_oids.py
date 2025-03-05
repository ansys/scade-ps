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

"""Test suite for change_oids.py."""

import pytest

from conftest import get_resources_dir, run_tool


@pytest.mark.parametrize('dump_paths', [False, True])
def test_find_duplicates_nominal(dump_paths, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'ChangeOids'
    models_dir = base_dir / 'models'
    projects = [models_dir / _ / (_ + '.etp') for _ in ['P1', 'P2', 'P3']]

    args = ['find', '-p'] + [str(_) for _ in projects]
    if dump_paths:
        args.extend(['-d', '-x', '.duppaths.txt'])
        ref = base_dir / 'ref' / 'find_duplicates' / 'paths'
    else:
        ref = base_dir / 'ref' / 'find_duplicates' / 'oids'
    status = run_tool('ansys.scade.ps.change_oids', args, ref, models_dir)
    assert status.returncode == 0


def test_change_oids_robustness():
    """
    Run the module with an unknown command.

    Use the executable to complete the coverage of __main__.py.
    """
    base_dir = get_resources_dir() / 'resources' / 'ChangeOids'
    path_src = base_dir / 'models' / 'P1' / 'P1.etp'

    args = ['-p', str(path_src), 'unknown']
    status = run_tool('ansys_scade_ps_change_oids.exe', args, None, None)
    assert status.returncode == 2

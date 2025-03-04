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

"""
Test suite for rename_unused.py.

Test strategy:

Run the tool on a directory and check the list of renamed files.
"""

import pytest

from conftest import get_resources_dir, load_tmp_project, run_tool


@pytest.mark.parametrize('base', ['Nominal'])
def test_rename_unused_nominal(base, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'RenameUnused' / base
    source = base_dir / 'model' / (base + '.etp')
    target_dir = local_tmpdir / 'test_rename_unused_nominal' / base
    project = load_tmp_project(source, target_dir)
    # options
    ref = base_dir / 'ref'
    args = ['-p', project.pathname]
    status = run_tool('ansys.scade.ps.rename_unused', args, ref, target_dir)
    assert status.returncode == 0


def test_rename_unused_robustness():
    args = []
    status = run_tool('ansys_scade_ps_rename_unused.exe', args)
    assert status.returncode == 2

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
Test suite for default_notes.py.

Test strategy:

The tests of this module make a copy of a reference project, create default notes
and add compare the result files to a reference.
"""

from pathlib import Path
import subprocess
import sys

import pytest

from conftest import load_tmp_project
from test_utils import diff_directories, diff_files, get_resources_dir


def _run_default_notes(src: Path, expected: int, ref: Path, dst: Path):
    """
    Run default_notes with the specified command-line parameters.

    The test is successful if:

    * the return code is the expected one
    * the produced files are identical to the reference ones
    """
    cmd = [
        sys.executable,
        '-m',
        'ansys.scade.ps.default_notes',
        '-p',
        str(src),
    ]
    status = subprocess.run(cmd, capture_output=True)
    if status.stderr:
        print(status.stderr.decode('utf-8').strip('\n'))
    if status.stdout:
        print(status.stdout.decode('utf-8').strip('\n'))
    assert status.returncode == expected
    if expected == 0:
        # no error, compare files
        if ref.is_dir():
            failure = diff_directories(ref, dst)
        else:
            failure = diff_files(ref, dst)
        assert not failure


@pytest.mark.parametrize('base', ['Nominal'])
def test_default_notes_nominal(base, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'DefaultNotes' / base
    source = base_dir / 'model' / (base + '.etp')
    target_dir = local_tmpdir / 'test_default_notes_nominal' / base
    project = load_tmp_project(source, target_dir)
    # get the reference directory
    ref_dir = base_dir / 'reference'
    # create default notes
    _run_default_notes(Path(project.pathname), 0, ref_dir, target_dir)


def test_default_notes_empty(local_tmpdir):
    """Empty is a model with no annotation schema."""
    base = 'Empty'
    base_dir = get_resources_dir() / 'resources' / 'DefaultNotes' / base
    source = base_dir / 'model' / (base + '.etp')
    target_dir = local_tmpdir / 'test_default_notes_empty' / base
    project = load_tmp_project(source, target_dir)

    # reset captured output
    cmd = [
        str(Path(sys.executable).with_name('ansys_scade_ps_default_notes.exe')),
        '-p',
        project.pathname,
    ]
    status = subprocess.run(cmd, capture_output=True)
    assert status.returncode == 0
    failure = False
    if status.stderr:
        print(status.stderr.decode('utf-8').strip('\n'))
        failure = True
    if status.stdout:
        print(status.stdout.decode('utf-8').strip('\n'))
        failure = True
    # nothing should have been reported
    assert not failure
    # neither created
    ann_files = [_ for _ in (target_dir).glob('**/*.ann')]
    assert not ann_files

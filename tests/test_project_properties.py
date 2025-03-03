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
from typing import List

import pytest

from conftest import load_tmp_project
from test_utils import diff_files, get_resources_dir


def _run_properties(src: Path, args: List[str], expected: int, ref: Path, dst: Path):
    """
    Run project properties with the specified command-line parameters.

    The test is successful if:

    * the return code is the expected one
    * the produced file is identical to the reference
    """
    cmd = [
        sys.executable,
        '-m',
        'ansys.scade.ps.project_properties',
        '-p',
        str(src),
    ]
    cmd.extend(args)
    status = subprocess.run(cmd, capture_output=True)
    if status.stderr:
        print(status.stderr.decode('utf-8').strip('\n'))
    if status.stdout:
        print(status.stdout.decode('utf-8').strip('\n'))
    assert status.returncode == expected
    if expected == 0:
        # no error, compare files
        failure = diff_files(ref, dst)
        assert not failure


@pytest.mark.parametrize('base', ['Model'])
def test_create_template_nominal(capsys, base, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'ProjectProperties'
    source = base_dir / base / (base + '.etp')
    target_dir = local_tmpdir / 'test_project_properties'
    target_dir.mkdir(exist_ok=True, parents=True)
    # options
    template = target_dir / 'model_template.json'
    ref = base_dir / 'ref' / template.name

    args = ['template', '-o', str(template)]
    _run_properties(Path(source), args, 0, ref, template)


@pytest.mark.parametrize(
    'target, expected',
    [
        ('Copy', 0),
        ('Unchanged', 0),
        ('NoSchema', 1),
    ],
)
def test_copy_properties_nominal(target: str, expected: int, local_tmpdir):
    """Copy the properties specified in schema.json from Model to the target project."""
    base_dir = get_resources_dir() / 'resources' / 'ProjectProperties'
    path_src = base_dir / 'Model' / 'Model.etp'
    target_dir = local_tmpdir / 'test_project_properties' / target
    dst = load_tmp_project(base_dir / target / f'{target}.etp', target_dir)
    ref = base_dir / 'ref' / f'{target}.etp'
    # options
    schema = target_dir / 'schema.json'

    args = ['copy', '-p', dst.pathname, '-s', str(schema)]
    _run_properties(path_src, args, expected, ref, Path(dst.pathname))


def test_project_properties_robustness():
    """
    Run the module with an unknown command.

    Use the executable to complete the coverage of __main__.py.
    """
    base_dir = get_resources_dir() / 'resources' / 'ProjectProperties'
    path_src = base_dir / 'Model' / 'Model.etp'

    cmd = [
        Path(sys.executable).with_name('ansys_scade_ps_project_properties.exe'),
        '-p',
        str(path_src),
        'unknown',
    ]
    status = subprocess.run(cmd, capture_output=True)
    if status.stderr:
        print(status.stderr.decode('utf-8').strip('\n'))
    if status.stdout:
        print(status.stdout.decode('utf-8').strip('\n'))
    assert status.returncode != 0

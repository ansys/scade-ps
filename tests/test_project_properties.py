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

import pytest

from conftest import get_resources_dir, load_tmp_project, run_tool


@pytest.mark.parametrize('base', ['Model'])
def test_create_template_nominal(capsys, base, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'ProjectProperties'
    source = base_dir / base / (base + '.etp')
    target_dir = local_tmpdir / 'test_project_properties'
    target_dir.mkdir(exist_ok=True, parents=True)
    # options
    template = target_dir / 'model_template.json'
    ref = base_dir / 'ref' / template.name

    args = ['-p', str(source), 'template', '-o', str(template)]
    status = run_tool('ansys.scade.ps.project_properties', args, ref, template)
    assert status.returncode == 0


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

    args = ['-p', str(path_src), 'copy', '-p', dst.pathname, '-s', str(schema)]
    status = run_tool('ansys.scade.ps.project_properties', args, ref, Path(dst.pathname))
    assert status.returncode == expected


def test_project_properties_robustness():
    """
    Run the module with an unknown command.

    Use the executable to complete the coverage of __main__.py.
    """
    base_dir = get_resources_dir() / 'resources' / 'ProjectProperties'
    path_src = base_dir / 'Model' / 'Model.etp'

    args = ['-p', str(path_src), 'unknown']
    status = run_tool('ansys_scade_ps_project_properties.exe', args, None, None)
    assert status.returncode == 2

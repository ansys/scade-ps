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

import pytest

from ansys.scade.ps.project_properties.copy_properties import CopyProperties
from ansys.scade.ps.project_properties.create_template import CreateTemplate
from conftest import load_project, load_tmp_project
from test_utils import cmp_file, get_resources_dir


@pytest.mark.parametrize('base', ['Model'])
def test_create_template_nominal(capsys, base, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'ProjectProperties'
    source = base_dir / base / (base + '.etp')
    project = load_project(source)
    target_dir = local_tmpdir / 'test_project_properties'
    target_dir.mkdir(exist_ok=True, parents=True)
    ref_dir = base_dir / 'ref'
    # options
    template = target_dir / 'model_template.json'
    # create template
    cls = CreateTemplate(str(template))
    status = cls.main(project)
    assert status == 0
    # reset captured output
    captured = capsys.readouterr()
    try:
        diff = cmp_file(ref_dir / template.name, template, n=0)
    except BaseException as e:
        diff = [str(e)]
    # not captured, thus the loop hereafter
    # stdout.writelines(diff)
    for line in diff:
        print(line, end='')
    captured = capsys.readouterr()
    assert captured.out == ''


@pytest.mark.parametrize('target', ['Copy', 'Unchanged'])
def test_copy_properties_nominal(capsys, target, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'ProjectProperties'
    src = load_project(base_dir / 'Model' / 'Model.etp')
    target_dir = local_tmpdir / 'test_project_properties' / target
    dst = load_tmp_project(base_dir / target / f'{target}.etp', target_dir)
    ref_dir = base_dir / 'ref'
    # options
    schema = target_dir / 'schema.json'
    # copy properties
    cls = CopyProperties(str(schema))
    status = cls.main(src, [dst])
    assert status == 0
    # reset captured output
    captured = capsys.readouterr()
    try:
        diff = cmp_file(ref_dir / f'{target}.etp', target_dir / f'{target}.etp', n=0)
    except BaseException as e:
        diff = [str(e)]
    # not captured, thus the loop hereafter
    # stdout.writelines(diff)
    for line in diff:
        print(line, end='')
    captured = capsys.readouterr()
    assert captured.out == ''

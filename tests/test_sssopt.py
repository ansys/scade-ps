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

"""Unit tests for sss scenario optimization."""

from pathlib import Path

import pytest
import scade.model.suite as suite

from ansys.scade.ps.optimize_sss.sssopt import _main as sssopt_main
from conftest import cmp_file, load_session


@pytest.fixture(scope='session')
def model_ro() -> suite.Model:
    """Load a read-only model."""
    test_dir = Path(__file__).parent
    path = test_dir / 'resources/OptimizeSss/Nominal/Model/Model.etp'
    session = load_session(path)
    return session.model


@pytest.mark.parametrize(
    'case',
    [('Nominal/Test/A.sss', 'Nominal/Test/S1.sss'), ('Nominal/Test/A.sss', 'Nominal/Test/S2.sss')],
)
def test_sss_opt(model_ro, tmpdir, case, capsys):
    base_alias, base_scenario = case

    test_dir = Path(__file__).parent
    alias = test_dir / 'resources/OptimizeSss' / base_alias
    scenario = test_dir / 'resources/OptimizeSss' / base_scenario

    basename = scenario.with_suffix('.csv').name
    output = Path(tmpdir) / basename
    ref = test_dir / 'ref' / 'OptimizeSss' / basename

    print('scenario', scenario)
    print('alias', alias)
    print('output', output)
    sssopt_main(model_ro, scenario, alias, str(output))

    # ignore any message issued prior this text: banner, warnings, etc.
    captured = capsys.readouterr()
    diff = cmp_file(ref, output, n=0)
    for line in list(diff):
        print(line, end='')
    # stdout.writelines(diff)
    captured = capsys.readouterr()
    assert captured.out == ''

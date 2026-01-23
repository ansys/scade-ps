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

"""Unit tests for scade utilities."""

from pathlib import Path

import pytest
import scade.model.suite as suite

import ansys.scade.ps.optimize_sss.scutils as scutils
from conftest import load_session


@pytest.fixture(scope='session')
def model_ro() -> suite.Model:
    """Load a read-only model."""
    test_dir = Path(__file__).parent
    path = test_dir / 'resources/OptimizeSss/Nominal/Model/Model.etp'
    session = load_session(path)
    return session.model


@pytest.mark.parametrize(
    'path',
    [
        ('P::O/v1[0].a.b[2][3].c[4]', ('P::O/v1', [0, 'a', 'b', 2, 3, 'c', 4])),
        ('P::O/v1.ab.cd[2][3].ef', ('P::O/v1', ['ab', 'cd', 2, 3, 'ef'])),
        ('P::O/v1', ('P::O/v1', [])),
    ],
)
def test_split_path(path):
    r = scutils.split_path(path[0])
    print(r)
    assert r == path[1]


@pytest.mark.parametrize(
    'case',
    [
        ('scalar', ['scalar']),
        ("','", ["','"]),
        ('(a, 2, bb)', ['(', 'a', ',', '2', ',', 'bb', ')']),
    ],
)
def test_splitex(case):
    text, tree = case
    assert scutils.splitex(text, '(),') == tree


@pytest.mark.parametrize(
    'case',
    [
        ('scalar', 'scalar'),
        ('(a, 2, bb)', ['a', '2', 'bb']),
        ('(1, 2, (3, 4), (5, (6, 77, 9)))', ['1', '2', ['3', '4'], ['5', ['6', '77', '9']]]),
    ],
)
def test_value_to_tree(case):
    text, tree = case
    v = scutils.value_to_tree(text)
    assert v == tree


@pytest.mark.parametrize(
    'case',
    [
        ('scalar', 'scalar', ''),
        ('scalarnew', 'scalar', 'scalarnew'),
        (['a', 2, 'bb'], ['a', 2, 'bb'], ''),
        (['a', 2, 'b'], ['a', 2, 'bb'], ['', '', 'b']),
        (
            [1, 2, [3, 4], [55, ['?', '?', '?']]],
            [1, 2, [3, 4], [5, ['a', 'b', 'c']]],
            ['', '', '', [55, '?']],
        ),
        (['?', '?', ['?', '?'], ['?', ['?', '?', '?']]], [1, 2, [3, 4], [5, ['a', 'b', 'c']]], '?'),
    ],
)
def test_reduce_value(case):
    value, reference, result = case
    assert scutils.reduce_value(value, reference) == result


@pytest.mark.parametrize(
    'case',
    [
        ('scalar', 'scalar'),
        ('(a,2,bb)', ['a', '2', 'bb']),
        ("(a,2,'(')", ['a', '2', "'('"]),
        ('(1,2,(3,4),(5,(6,77,9)))', ['1', '2', ['3', '4'], ['5', ['6', '77', '9']]]),
    ],
)
def test_tree_to_str(case):
    text, tree = case
    t = scutils.tree_to_str(tree)
    assert t == text


@pytest.mark.parametrize(
    'case', [('P::BIG/', '(,,,(,,),(,,))'), ('P::E/', ''), ('P::S/', '(,,)'), ('P::T/', '(,,)')]
)
def test_get_default_value(model_ro, case):
    path, default = case
    type_ = model_ro.get_object_from_path(path)
    assert scutils.tree_to_str(scutils.get_default_value(type_)) == default


@pytest.mark.parametrize(
    'case',
    [
        ('?', 'P::BIG/', ['?', '?', '?', ['?', '?', '?'], ['?', '?', '?']]),
        (
            ['1', '2', '3', '?', ['4', '?', '5']],
            'P::BIG/',
            ['1', '2', '3', ['?', '?', '?'], ['4', '?', '5']],
        ),
        (
            ['1', '2', '3', ['4', '?', '5'], '?'],
            'P::BIG/',
            ['1', '2', '3', ['4', '?', '5'], ['?', '?', '?']],
        ),
    ],
)
def test_adjust_default_value(model_ro, case):
    value, path, result = case
    type_ = model_ro.get_object_from_path(path)
    assert scutils.adjust_value(value, type_) == result


@pytest.mark.parametrize('case', [('P::BIG/', 9), ('P::E/', 1), ('P::S/', 3), ('P::T/', 3)])
def test_get_type_width(model_ro, case):
    path, result = case
    type_ = model_ro.get_object_from_path(path)
    assert scutils.get_type_width(type_) == result


@pytest.mark.parametrize(
    'case',
    [
        ('P::BIG/', ['b'], 0, suite.NamedType),
        ('P::BIG/', ['t', 2], 2, suite.NamedType),
        ('P::BIG/', ['t'], 3, suite.Table),
        ('P::BIG/', ['s'], 4, suite.Structure),
        ('P::BIG/', ['s', 'x'], 1, suite.NamedType),
    ],
)
def test_resolve_path(model_ro, case):
    pathtype, path, result, cls = case
    type_ = model_ro.get_object_from_path(pathtype)
    _, index, subtype = scutils.resolve_path(scutils.get_default_value(type_), type_, path)
    assert index == result
    assert type(scutils.get_type_definition(subtype)) is cls


@pytest.mark.parametrize(
    'case',
    [
        (['a', 'b', 'c', 'd'], [-1, 1, 0, 2], ['a', 'b', '?', 'd'], [-1, 0, -1, 1], 1),
        (['a', 'b', ['c', 'd']], [-1, 0, [0, 1]], ['a', '?', ['?', 'd']], [-1, -1, [-1, 0]], 2),
    ],
)
def test_apply_sustain(case):
    value_i, sustain_i, value_o, sustain_o, n_o = case
    n = scutils.apply_sustain(value_i, sustain_i)
    assert value_i == value_o
    assert sustain_i == sustain_o
    assert n == n_o

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

"""Set of utilities."""

from functools import reduce
from re import compile
from typing import List, Sequence, Tuple, Union

from scade.model.suite import NamedType, Structure, Table, Type

LiteralTree = Union[List, str]
"""
Annotation type for scenario values: hierarchy of literal values.
"""


CounterTree = Union[List, int]
"""
Annotation type for sustain counters associated to a scenario value: hierarchy of integers.
"""

# annotation types for utilities common to literal and counter trees
Leaf = Union[str, int]
Tree = Union[LiteralTree, CounterTree]
SubPath = Sequence[Union[str, int]]


def get_type_definition(type_: Type) -> Type:
    """Return the leaf type of a type."""
    if isinstance(type_, NamedType) and not type_.is_predefined():
        return get_type_definition(type_.type)

    return type_


def resolve_path(tree: list, type_: Type, path: SubPath) -> Tuple[list, int, Type]:
    """Return the list containing the last path element, its index and type."""
    subtree = tree
    for elem in path:
        tree = subtree
        # skip aliases
        type_ = get_type_definition(type_)
        # following assert failure(s) implies an error in the scenario
        if isinstance(type_, Table):
            # assert len(subtree) == type_.size
            type_ = type_.type
            # elem must be an integer
            index = int(elem)
        elif isinstance(type_, Structure):
            # assert len(subtree) == len(type_.elements)
            for index, field in enumerate(type_.elements):
                # optimization: add a cache in the type?
                if field.name == elem:
                    index = field.element_range
                    break
            else:
                # not existing field
                raise ValueError(f'{type_.get_full_path()}: unknown {elem} field')
            type_ = field.type
        else:
            raise ValueError(f'{type_.get_full_path()}: value mismatch')
        subtree = tree[index]

    return tree, index, type_


def adjust_value(value: LiteralTree, type_: Type) -> LiteralTree:
    """Replace ``?`` placeholders for tables/structures by trees, bypassing aliases."""
    type_ = get_type_definition(type_)
    if value == '?':
        return get_default_value(type_, '?')  # type: ignore
    if isinstance(type_, Table):
        if not isinstance(value, list) or len(value) != type_.size:
            raise ValueError(f'{type_.get_full_path()}: value mismatch')
        return [adjust_value(cell, type_.type) for cell in value]
    elif isinstance(type_, Structure):
        if not isinstance(value, list) or len(value) != len(type_.elements):
            raise ValueError(f'{type_.get_full_path()}: value mismatch')
        return [
            adjust_value(subvalue, element.type)
            for subvalue, element in zip(value, type_.elements, strict=True)
        ]
    else:
        return value


def patch_tree(
    tree: list, value: LiteralTree, type_: Type, path: Sequence[Union[str, int]], needadjust=False
):
    """Update a value of a tree."""
    tree, index, type_ = resolve_path(tree, type_, path)
    if needadjust:
        tree[index] = adjust_value(value, type_)
    else:
        tree[index] = value


def get_tree_width(tree: CounterTree) -> int:
    """Return the number of elements different from 0 of the flattened tree."""
    if isinstance(tree, list):
        width = reduce(lambda x, y: x + y, [get_tree_width(elem) for elem in tree])
    else:
        width = 1 if tree > 0 else 0
    return width


def patch_sustain(tree: list, sustain: int, type_: Type, path: SubPath) -> int:
    """Update the sustain value of a tree."""
    tree, index, type_ = resolve_path(tree, type_, path)
    old_width = get_tree_width(tree[index])
    tree[index] = get_default_value(type_, sustain)
    new_width = get_type_width(type_) if sustain > 0 else 0
    return new_width - old_width


def get_default_value(type_: Type, fill: object = '') -> Union[List, object]:
    """Return a tree corresponding to a type."""
    # skip aliases
    type_ = get_type_definition(type_)
    if isinstance(type_, Table):
        value = get_default_value(type_.type, fill)
        return [value] * type_.size
    elif isinstance(type_, Structure):
        return [get_default_value(field.type, fill) for field in type_.elements]
    else:
        return fill


_re_path = compile(r'([^\[\.]*)(.*)?')


def split_path(path: str) -> Tuple[str, Sequence[Union[str, int]]]:
    """
    Return the path identifying the semantic element and its subpath as a list: index and/or fields.

    ``path`` is expected to be a sensor or local variable, with optional subpath.
    """
    match = _re_path.match(path)
    assert match is not None  # nosec B101  # addresses linter
    var_path, sub_paths = match.groups()
    if sub_paths:
        items = sub_paths.replace('[', '.').replace(']', '').strip('.').split('.')
        items = [int(i) if i.isdecimal() else i for i in items]
    else:
        items = []

    return var_path, items


def splitex(text: str, separators: str) -> List[str]:
    """Return the list of tokens, including the separators."""
    # use `tok` instead of `token` so that bandit does not raise B105
    tok = ''
    result = []
    quote = False
    for c in text:
        if not quote and c in separators:
            tok = tok.strip()
            if tok != '':
                result.append(tok)
            tok = ''
            result.append(c)
        else:
            tok += c
            if c == "'":
                quote = not quote
    tok = tok.strip()
    if tok != '':
        result.append(tok)

    return result


def value_to_tree(value: str) -> LiteralTree:
    """Provide a tree representation of a structured value."""
    # use `tok[s]` instead of `token[s]` so that bandit does not raise B105
    toks = splitex(value, '()[],')
    tree = []
    current = []
    for tok in toks:
        if tok == ')' or tok == ']':
            pop = tree.pop()
            pop.append(current)
            current = pop
        elif tok == ',':
            pass
        elif tok == '(' or tok == '[':
            tree.append(current)
            current = []
        else:
            current.append(tok)

    return current[0] if current else ''


def reduce_value(value: LiteralTree, reference: LiteralTree) -> LiteralTree:
    """Remove from value parts identical to reference."""
    # value and reference must have the same tree structure
    if not isinstance(value, list):
        # leaf
        return '' if value == reference else value

    result = []
    empty = True
    dontcare = True
    for v, r in zip(value, reference):
        red = reduce_value(v, r)
        if red != '':
            empty = False
        if red != '?':
            dontcare = False
        result.append(red)

    return '' if empty else '?' if dontcare else result


def tree_to_str(value: Union[list, object]) -> str:
    """Serialize a tree to a string."""
    if isinstance(value, list):
        return '(' + ','.join([tree_to_str(v) for v in value]) + ')'
    else:
        # leaf
        return str(value)


# cache
_type_widths = {}


def get_type_width(type_: Type) -> int:
    """Return the number of leaves of the type tree."""
    # use a lazy cache to minimize the computations
    global _type_widths
    width = _type_widths.get(type_)
    if not width:
        if isinstance(type_, Table):
            width = type_.size * get_type_width(type_.type)
        elif isinstance(type_, Structure):
            width = reduce(
                lambda x, y: x + y, [get_type_width(field.type) for field in type_.elements]
            )
        elif isinstance(type_, NamedType) and not type_.is_predefined():
            width = get_type_width(type_.type)
        else:
            width = 1
        _type_widths[type_] = width
    return width


def apply_sustain(value: list, sustain: list) -> int:
    """
    Return the number of obsolete checks when removing one to positive sustain values.

    Set a corresponding value to '?' when its counter becomes null
    """
    count = 0
    # assert len(value) == len(sustain)
    for i, element in enumerate(sustain):
        if isinstance(element, list):
            count += apply_sustain(value[i], sustain[i])
        elif element >= 0:
            if element == 0:
                value[i] = '?'
                count += 1
            sustain[i] -= 1

    return count

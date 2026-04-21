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

"""
Python library for Scenario Optimizer.

DO NOT EDIT GENERATED BLOCKS, delimited by ``{{`` and ``}}`` markers.
"""

#%% begin

#%% import

from copy import deepcopy
from pathlib import Path
from typing import List, Optional, Sequence as Seq, Union

# aliases used in ecore references
import scade.model.suite as suite
from scade.model.suite import ConstVar as ScConstVar, Model as ScModel, Object as ScObject

from ansys.scade.ps.optimize_sss.scenparser import SSSParser
from ansys.scade.ps.optimize_sss.scutils import (
    CounterTree,
    LiteralTree,
    adjust_value,
    apply_sustain,
    get_default_value,
    get_type_width,
    patch_sustain,
    patch_tree,
    split_path,
    value_to_tree,
)

# ---------------------------------------------------------------------------
# model
# ---------------------------------------------------------------------------

#%% types

'''
# unused declaration
#{{type(78)
class AliasTable:
    pass
#}}type

#{{type(159)
class SubPath:
    pass
#}}type

#{{type(148)
class ValueTree:
    pass
#}}type
'''


AliasTable = dict
SubPath = Union[Seq[Union[str, int]], None]


class ValueTreeImpl:
    """
    Value as a tree structure.

    Each node is either a literal value, as a string, or a list of nodes.

    .. Notes::

      * `'?`'` represents any sub-tree
      * `''` represents an error in the scenario or an uninitialized value
    """

    def __init__(self, value: str = ''):
        self.tree: LiteralTree = value_to_tree(value)
        # the string value may not be complete with respect of the type
        # for example, '?' instead of (1, 2, 3)
        self.needadjust = '?' in value

    @property
    def scalar(self) -> bool:
        return not isinstance(self.tree, list)

    def clone(self) -> 'ValueTreeImpl':
        clone = ValueTreeImpl()
        clone.tree = deepcopy(self.tree)
        # clone.tree = self.value if self.scalar else self.value.copy()
        clone.needadjust = self.needadjust
        return clone

    def patch(self, value: 'ValueTreeImpl', io: 'IO', path: SubPath):
        # Update a value or sub-value of a variable.
        assert io.constvar is not None  # nosec B101  # addresses linter
        patch = value.tree.copy() if isinstance(value.tree, list) else value.tree
        if path:
            assert isinstance(self.tree, list)  # nosec B101  # addresses linter
            patch_tree(self.tree, patch, io.constvar.type, path, needadjust=value.needadjust)
        else:
            if value.needadjust:
                self.tree = adjust_value(patch, io.constvar.type)
            else:
                self.tree = patch

    @classmethod
    def default(cls, type_: suite.Type, fill: str = '') -> 'ValueTreeImpl':
        default = ValueTreeImpl()
        tree = get_default_value(type_, fill)
        default.tree = tree  # type: ignore
        return default

ValueTree = Optional[ValueTreeImpl]

class SustainTree:
    """
    Value as a tree structure.

    Each node is either a literal value, as a string, or a list of nodes.

    .. Notes::

      * `'?`'` represents any sub-tree
      * `''` represents an error in the scenario or an uninitialized value
    """

    def __init__(self, type_: suite.Type):
        self.tree: CounterTree = get_default_value(type_, 0)  # type: ignore
        # number of active checks
        # self.check_count = get_type_width(type_)
        self.check_count = 0

    def patch(self, sustain: int, io: 'IO', path: SubPath):
        assert io.constvar is not None  # nosec B101  # addresses linter
        if path:
            assert isinstance(self.tree, list)  # nosec B101  # addresses linter
            offset = patch_sustain(self.tree, sustain, io.constvar.type, path)
            self.check_count += offset
        else:
            tree = get_default_value(io.constvar.type, sustain)
            self.tree = tree  # type: ignore
            self.check_count = get_type_width(io.constvar.type) if sustain > 0 else 0

    @property
    def active(self) -> bool:
        return self.check_count > 0

    def apply(self, value: ValueTreeImpl) -> bool:
        # assert self.active
        if isinstance(self.tree, list):
            assert isinstance(value.tree, list)  # nosec B101  # addresses linter
            offset = apply_sustain(value.tree, self.tree)
        else:
            offset = 0
            if self.tree >= 0:
                if self.tree == 0:
                    value.tree = '?'
                    offset = 1
                self.tree -= 1
        self.check_count -= offset
        return offset > 0


#%% classes

#{{class(63)
class ScadeProxy:
    def __init__(self):
        self.scelement: Optional[ScObject] = None

    def bind(self, model: 'Optional[ScObject]'):
        #<<132
        # abstract function
        raise NotImplementedError()
        #>>132
#}}class


#{{class(11)
class IO(ScadeProxy):
    def __init__(self, alias: str = ''):
        super().__init__()
        self.directives: List[Directive] = []
        self.sequence: Optional[Sequence] = None
        self.alias: str = alias
        #<<init
        # runtime values: reference and current values for output optimization
        self._reference: ValueTree = None
        self._value: ValueTree = None
        self._tol_reference = ''
        self._tol_value = ''
        # individual counters for checks: same tree structure as _reference/_value
        # 0: sustain just ended
        # >0 sustain active
        # -1 forever
        self._sustain: Optional[SustainTree] = None
        # number of active individual checks (scalar values)
        self._active_checks = 0
        #>>init

    @property
    def constvar(self) -> 'Optional[ScConstVar]':
        #<<99
        return self.scelement
        #>>99

    def bind(self, model: 'Optional[ScConstVar]'):
        #<<93
        self.scelement = model
        #>>93

    def is_output(self) -> bool:
        #<<151
        assert self.constvar is not None  # nosec B101  # addresses linter
        return self.constvar.is_output() or self.constvar.probe
        #>>151

    def add_directive(self, directive: 'Directive'):
        self.directives.append(directive)
        directive.io = self

    def set_sequence(self, sequence: 'Sequence'):
        self.sequence = sequence
        sequence.ios.append(self)

    #<<cls
    # properties to limit linter issues

    @property
    def value_tree(self) -> LiteralTree:
        assert self._value is not None  # nosec B101  # addresses linter
        return self._value.tree

    @property
    def reference_tree(self) -> LiteralTree:
        assert self._reference is not None  # nosec B101  # addresses linter
        return self._reference.tree
    #>>cls
#}}class


#{{class(155)
class Directive:
    def __init__(self, path: SubPath = None):
        self.step: Optional[Step] = None
        self.io: Optional[IO] = None
        self.path: SubPath = path

    def patch_io(self):
        #<<156
        # to be considered as abstract
        raise NotImplementedError()
        #>>156

    def set_step(self, step: 'Step'):
        self.step = step
        step.directives.append(self)

    def set_io(self, io: 'IO'):
        self.io = io
        io.directives.append(self)
#}}class


#{{class(36)
class SetCheck(Directive):
    def __init__(self, path: SubPath = None, value_tree: ValueTree = None):
        super().__init__(path)
        self.value_tree: ValueTree = value_tree

    def patch_io(self):
        #<<149
        assert self.value_tree is not None  # nosec B101  # addresses linter
        # assert self.path is not None  # nosec B101  # addresses linter
        assert self.io is not None  # nosec B101  # addresses linter
        assert self.io._value is not None  # nosec B101  # addresses linter
        self.io._value.patch(self.value_tree, self.io, self.path)
        #>>149
#}}class


#{{class(41)
class Check(SetCheck):
    def __init__(self, path: SubPath = None, value_tree: ValueTree = None, sustain: int = 0, tolerance: str = ''):
        super().__init__(path, value_tree)
        self.sustain: int = sustain
        self.tolerance: str = tolerance

    def patch_io(self):
        #<<150
        super().patch_io()
        assert self.io is not None  # nosec B101  # addresses linter
        assert self.io.constvar is not None  # nosec B101  # addresses linter
        assert self.io._sustain is not None  # nosec B101  # addresses linter
        self.io._sustain.patch(self.sustain, self.io, self.path)
        if self.tolerance:
            print('tolerance associated to a check not supported for', self.io.constvar.get_full_path())
        #>>150
#}}class


#{{class(39)
class Set(SetCheck):
    def __init__(self, path: SubPath = None, value_tree: ValueTree = None):
        super().__init__(path, value_tree)
#}}class


#{{class(152)
class Tolerance(Directive):
    def __init__(self, path: SubPath = None, tolerance: str = ''):
        super().__init__(path)
        self.tolerance: str = tolerance

    def patch_io(self):
        #<<153
        assert self.io is not None  # nosec B101  # addresses linter
        self.io._tol_value = self.tolerance
        #>>153
#}}class


#{{class(8)
class Step:
    def __init__(self, tolerance: str = '', cycles: int = 0):
        self.tolerance: str = tolerance
        self.comments: List[str] = []
        self.cycles: int = cycles
        self.directives: List[Directive] = []
        self.scenario: Optional[Scenario] = None

    def add_directive(self, directive: 'Directive'):
        self.directives.append(directive)
        directive.step = self

    def set_scenario(self, scenario: 'Scenario'):
        self.scenario = scenario
        scenario.steps.append(self)
#}}class


#{{class(2)
class Scenario:
    def __init__(self, pathname: str = ''):
        self.pathname: str = pathname
        self.steps: List[Step] = []
        self.sequence: Optional[Sequence] = None

    def add_step(self, step: 'Step'):
        self.steps.append(step)
        step.scenario = self

    def set_sequence(self, sequence: 'Sequence'):
        self.sequence = sequence
        sequence.scenarios.append(self)
#}}class


#{{class(7)
class CsvScenario(Scenario):
    def __init__(self, pathname: str = ''):
        super().__init__(pathname)
#}}class


#{{class(6)
class SssScenario(Scenario):
    def __init__(self, pathname: str = ''):
        super().__init__(pathname)
#}}class


#{{class(74)
class Sequence:
    def __init__(self, aliases: AliasTable = {}):
        self.application: Optional[Application] = None
        self.scenarios: List[Scenario] = []
        self.aliases: AliasTable = aliases
        self.ios: List[IO] = []
        #<<init
        # actually, implemented as Dict[str, str]
        self.aliases = {}
        # additional dict for searches (TODO: ordered dict instead?)
        self._ios = {}	# type: Dict[str, IO]
        #>>init

    def load(self) -> bool:
        #<<136
        for scenario in self.scenarios:
            loader = None
            path = Path(scenario.pathname)
            if path.suffix.lower() == '.sss':
                loader = SssLoader(self, scenario)
            elif path.suffix.lower() == '.csv':
                print('CSV scenarios not supported:', path)
                return False
            else:
                print('Unknown scenario format:', path)
                return False

            if not loader.load(path):
                return False
        return True
        #>>136

    def create_scenario(self, pathname: str) -> 'Optional[Scenario]':
        #<<137
        path = Path(pathname)
        if path.suffix.lower() == '.sss':
            scenario = SssScenario()
            scenario.pathname = pathname
            # link
            self.add_scenario(scenario)
            return scenario
        return None
        #>>137

    def find_io(self, path: str) -> 'Optional[IO]':
        #<<145
        # lazy addition of a scenario IO (either IO, sensor or probe, we don't care)
        io = self._ios.get(path)
        if not io:
            assert self.application is not None  # nosec B101  # addresses linter
            assert self.application.model is not None  # nosec B101  # addresses linter
            var = self.application.model.get_object_from_path(path)
            assert var is not None  # nosec B101  # addresses linter
            io = IO()
            io.bind(var)
            io.alias = var.get_full_path().strip('/')
            # link
            self.add_io(io)
            # cache
            self._ios[path] = io

        return io
        #>>145

    def set_application(self, application: 'Application'):
        self.application = application
        application.sequences.append(self)

    def add_scenario(self, scenario: 'Scenario'):
        self.scenarios.append(scenario)
        scenario.sequence = self

    def add_io(self, io: 'IO'):
        self.ios.append(io)
        io.sequence = self
#}}class


#{{class(22)
class Application(ScadeProxy):
    def __init__(self):
        super().__init__()
        self.sequences: List[Sequence] = []

    @property
    def model(self) -> 'Optional[ScModel]':
        #<<116
        return self.scelement
        #>>116

    def bind(self, model: 'Optional[ScModel]'):
        #<<110
        self.scelement = model
        #>>110

    def add_sequence(self, sequence: 'Sequence'):
        self.sequences.append(sequence)
        sequence.application = self
#}}class

#%% declarations

#%% end

# ---------------------------------------------------------------------------
# utilities
# ---------------------------------------------------------------------------

class SssLoader(SSSParser):
    def __init__(self, sequence: Sequence, scenario: Scenario, **kwargs):
        super().__init__(**kwargs)
        self.sequence = sequence
        self.scenario = scenario
        self.aliases = sequence.aliases

        # current step (not linked yet)
        self.cycle = Step()


    def on_cycle(self, count: str):
        # register the current cycle and initialize a new one
        self.cycle.cycles = 1 if count is None else int(count)
        # link
        self.scenario.add_step(self.cycle)
        # new step
        self.cycle = Step()


    def on_set(self, path: str, value: str):
        set_ = Set()
        path = path.strip('{}')
        path = self.aliases.get(path, path)
        set_.value_tree = ValueTreeImpl(value.strip('{}'))
        # link
        self.cycle.add_directive(set_)
        # associated variable
        path_var, items = split_path(path)
        set_.io = self.sequence.find_io(path_var)
        # sub_path
        set_.path = items


    def on_check(self, path: str, value: str, sustain: str, real: str):
        check = Check()
        path = path.strip('{}')
        path = self.aliases.get(path, path)
        check.path = path
        check.value_tree = ValueTreeImpl(value.strip('{}'))
        check.sustain = 1 if sustain is None else -1 if sustain == 'forever' else int(sustain)
        check.tolerance = real
        # link
        self.cycle.add_directive(check)
        # associated variable
        path_var, items = split_path(path)
        check.io = self.sequence.find_io(path_var)
        # sub_path
        check.path = items


    def on_uncheck(self, path: str):
        # same as checking ? forever
        path = path.strip('{}')
        path = self.aliases.get(path, path)
        self.on_check(path, '?', 'forever', '')


    def on_set_tolerance(self, path: str, real: str):
        if path:
            # associated variable
            path = path.strip('{}')
            path = self.aliases.get(path, path)
            path_var, items = split_path(path)
            if items:
                print('tolerance not supported on partial values:', path)
            else:
                tol = Tolerance()
                tol.tolerance = real
                # link
                self.cycle.add_directive(tol)
                # associated variable
                tol.io = self.sequence.find_io(path_var)
        else:
            # TODO what happens if the tolerance is set twice in the same step?
            self.cycle.tolerance = real


    def on_alias(self, alias: str, path: str):
        path = path.strip('{}')
        self.aliases[alias] = path


    def on_comment(self, line: str):
        self.cycle.comments.append(line)

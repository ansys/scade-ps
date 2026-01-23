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
from typing import List, Dict, Optional

# aliases used in ecore references
import scade.model.suite as suite
from scade.model.suite import Object as ScObject, Model as ScModel, ConstVar as ScConstVar

from ansys.scade.ps.optimize_sss.scenparser import SSSParser
from ansys.scade.ps.optimize_sss.scutils import (
    split_path, value_to_tree,
    patch_tree,
    get_default_value,
    adjust_value,
    get_type_width,
    patch_sustain,
    apply_sustain,
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
'''


AliasTable = dict


#{{type(148)
class ValueTree:
    #<<cls
    def __init__(self, value: str = ''):
        self.value = value_to_tree(value) if value else None
        # the string value may not be complete with respect of the type
        # for example, '?' instead of (1, 2, 3)
        self.needadjust = False if value is None else '?' in value

    @property
    def scalar(self) -> bool:
        return not isinstance(self.value, list)

    def clone(self) -> 'ValueTree':
        clone = ValueTree()
        clone.value = deepcopy(self.value)
        #clone.value = self.value if self.scalar else self.value.copy()
        clone.needadjust = self.needadjust
        return clone

    def patch(self, value: 'ValueTree', io: 'IO', path: List[object]):
        # TODO: duplicated code from clone to not create a fake instance of ValueTree
        patch = value.value if value.scalar else value.value.copy()
        if path:
            patch_tree(self.value, patch, io.constvar.type, path, needadjust=value.needadjust)
        else:
            if value.needadjust:
                self.value = adjust_value(patch, io.constvar.type)
            else:
                self.value = patch

    @classmethod
    def default(cls, type_: suite.Type, fill: object = '') -> 'ValueTree':
        default = ValueTree()
        default.value = get_default_value(type_, fill)
        return default
    #>>cls
#}}type


class SustainTree:
    def __init__(self, type_: suite.Type):
        self.value = get_default_value(type_, 0)
        # number of active checks
        # self.check_count = get_type_width(type_)
        self.check_count = 0

    def patch(self, sustain: int, io: 'IO', path: List[object]):
        if path:
            offset = patch_sustain(self.value, sustain, io.constvar.type, path)
            self.check_count += offset
        else:
            self.value = get_default_value(io.constvar.type, sustain)
            self.check_count = get_type_width(io.constvar.type) if sustain > 0 else 0

    @property
    def active(self) -> bool:
        return self.check_count > 0

    def apply(self, value: ValueTree) -> bool:
        assert self.active
        if isinstance(self.value, list):
            offset = apply_sustain(value.value, self.value)
        else:
            offset = 0
            if self.value >= 0:
                if self.value == 0:
                    value.value = '?'
                    offset = 1
                self.value -= 1
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
        assert False
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
        self._reference: Optional[ValueTree] = None
        self._value: Optional[ValueTree] = None
        self._tol_reference = None  # type: str
        self._tol_value = ''    # type: str
        # individual counters for checks: same tree structure as _reference/_value
        # 0: sustain just ended
        # >0 sustain active
        # -1 forever
        self._sustain = None    # type: int
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
        return self.constvar.is_output() or self.constvar.probe
        #>>151

    def add_directive(self, directive: 'Directive'):
        self.directives.append(directive)
        directive.io = self

    def set_sequence(self, sequence: 'Sequence'):
        self.sequence = sequence
        sequence.ios.append(self)
#}}class


#{{class(155)
class Directive:
    def __init__(self, path: str = ''):
        self.step: Optional[Step] = None
        self.io: Optional[IO] = None
        self.path: str = path

    def patch_io(self):
        #<<156
        # to be considered as abstract
        assert False
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
    def __init__(self, path: str = '', value_tree: ValueTree = []):
        super().__init__(path)
        self.value_tree: ValueTree = value_tree

    def patch_io(self):
        #<<149
        self.io._value.patch(self.value_tree, self.io, self.path)
        #>>149
#}}class


#{{class(41)
class Check(SetCheck):
    def __init__(self, path: str = '', value_tree: ValueTree = [], sustain: int = 0, tolerance: str = ''):
        super().__init__(path, value_tree)
        self.sustain: int = sustain
        self.tolerance: str = tolerance

    def patch_io(self):
        #<<150
        super().patch_io()
        self.io._sustain.patch(self.sustain, self.io, self.path)
        if self.tolerance:
            print('tolerance associated to a check not supported for', self.io.constvar.get_full_path())
        #>>150
#}}class


#{{class(39)
class Set(SetCheck):
    def __init__(self, path: str = '', value_tree: ValueTree = []):
        super().__init__(path, value_tree)
#}}class


#{{class(152)
class Tolerance(Directive):
    def __init__(self, path: str = '', tolerance: str = ''):
        super().__init__(path)
        self.tolerance: str = tolerance

    def patch_io(self):
        #<<153
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
            self.scenarios.append(scenario)
            scenario.sequence = self
            return scenario
        return None
        #>>137

    def find_io(self, path: str) -> 'Optional[IO]':
        #<<145
        # lazy addition of a scenario IO (either IO, sensor or probe, we don't care)
        io = self._ios.get(path)
        if not io:
            var = self.application.model.get_object_from_path(path)
            assert var
            io = IO()
            io.bind(var)
            io.alias = var.get_full_path().strip('/')
            # link
            io.sequence = self
            self.ios.append(io)
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
        self.scenario.steps.append(self.cycle)
        self.cycle.scenario = self.scenario
        # new step
        self.cycle = Step()


    def on_set(self, path: str, value: str):
        set = Set()
        path = path.strip('{}')
        path = self.aliases.get(path, path)
        set.value_tree = ValueTree(value.strip('{}'))
        # link
        self.cycle.directives.append(set)
        set.step = self.cycle
        # associated variable
        path_var, items = split_path(path)
        set.io = self.sequence.find_io(path_var)
        # sub_path
        set.path = items


    def on_check(self, path: str, value: str, sustain: str, real: str):
        check = Check()
        path = path.strip('{}')
        path = self.aliases.get(path, path)
        check.path = path
        check.value_tree = ValueTree(value.strip('{}'))
        check.sustain = 1 if sustain is None else -1 if sustain == 'forever' else int(sustain)
        check.tolerance = real
        # link
        self.cycle.directives.append(check)
        check.step = self.cycle
        # associated variable
        path_var, items = split_path(path)
        check.io = self.sequence.find_io(path_var)
        # sub_path
        check.path = items


    def on_uncheck(self, path: str):
        # same as checking ? forever
        path = path.strip('{}')
        path = self.aliases.get(path, path)
        self.on_check(path, '?', 'forever', None)


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
                self.cycle.directives.append(tol)
                tol.step = self.cycle
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

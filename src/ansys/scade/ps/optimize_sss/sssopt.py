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

"""Optimization of a sss scenario to a csv scenario."""

from pathlib import Path

from scade.model.suite import Model, get_roots as get_sessions

from ansys.scade.ps.optimize_sss.scenario import (
    Application,
    Scenario,
    Sequence,
    SustainTree,
    ValueTreeImpl,
)
from ansys.scade.ps.optimize_sss.scutils import reduce_value, tree_to_str


def save_as_csv(scenario: Scenario, pathname: str):
    """Save a scenario to a CSV file."""

    def flush_line(last: bool = False):
        """Flush a line."""
        nonlocal buffer_line, buffer_cycles

        line = ';'.join(cells)
        empty_line = line.strip(';') == ''
        line_tols = ';'.join(tolerances)
        empty_tolerance = line_tols.strip(';') == ''
        if buffer_line:
            if not last and empty_tolerance and empty_line and not comments:
                # empty line: same as before
                buffer_cycles += cycles
                return

            # flush buffered line
            if last:
                f.write('Last')
                f.write(';' if buffer_cycles == 1 else ', Repeat %d;' % buffer_cycles)
            else:
                f.write(';' if buffer_cycles == 1 else 'Repeat %d;' % buffer_cycles)
            f.write(buffer_line)
            f.write('\n')

        if not last:
            for comment in comments:
                f.write('%s\n' % comment)

            if not empty_tolerance:
                f.write('Tol;')
                f.write(line_tols)
                f.write('\n')

        # buffer next line
        buffer_line = line
        buffer_cycles = cycles

    # cache for flush_line
    buffer_line = None
    buffer_cycles = 0

    # support only usual format: step by lines (format 0)
    assert scenario.sequence is not None  # nosec B101  # addresses linter
    sequence = scenario.sequence
    path = Path(pathname)
    try:
        # exist_ok added in 3.5
        path.parent.mkdir(parents=True, exist_ok=True)
    except BaseException:
        pass
    with path.open('w') as f:
        # header
        f.write('#$CsvFormat=0\n')
        # runtime values: current and reference
        for io in sequence.ios:
            assert io.constvar is not None  # nosec B101  # addresses linter
            io._reference = None
            io._value = ValueTreeImpl.default(io.constvar.type)
        # outputs: separate list with mask initialized to 0 (no check)
        os = [io for io in sequence.ios if io.is_output()]
        for o in os:
            assert io.constvar is not None  # nosec B101  # addresses linter
            o._sustain = SustainTree(io.constvar.type)
            o._active_checks = 0

        # head row
        f.write('*SCRIPT*;')
        f.write(';'.join([io.alias for io in sequence.ios]))
        f.write('\n')

        for step in scenario.steps:
            comments = step.comments

            # default values for the current step: previous ones
            for io in sequence.ios:
                assert io._value is not None  # nosec B101  # addresses linter
                io._reference = io._value
                io._value = io._reference.clone()
                io._tol_reference = io._tol_value
                # no need to clone _tol_value: str

            # patch current values with the directive
            for d in step.directives:
                d.patch_io()

            # apply active sustain
            for o in os:
                assert o._sustain is not None  # nosec B101  # addresses linter
                if o._sustain.active:
                    assert isinstance(o._value, ValueTreeImpl)  # nosec B101  # addresses linter
                    o._sustain.apply(o._value)

            # current row
            cells = [
                tree_to_str(reduce_value(io.value_tree, io.reference_tree)) for io in sequence.ios
            ]
            if step.tolerance:
                # patch tolerance for outputs w/o tolerance
                for o in os:
                    if not o._tol_value:
                        o._tol_value = step.tolerance
            tolerances = [
                '' if io._tol_value == io._tol_reference else io._tol_value for io in sequence.ios
            ]

            # split cycles if some checks become obsolete
            cycles = 1
            for i in range(step.cycles - 1):
                changed = False
                # default values for the current cycle: previous ones
                for io in sequence.ios:
                    assert io._value is not None  # nosec B101  # addresses linter
                    io._reference = io._value
                    io._value = io._reference.clone()

                for o in os:
                    assert o._sustain is not None  # nosec B101  # addresses linter
                    if o._sustain.active:
                        assert isinstance(o._value, ValueTreeImpl)  # nosec B101  # addresses linter
                        if o._sustain.apply(o._value):
                            # the current cells must be flushed
                            changed = True

                if changed:
                    # flushed buffered line
                    flush_line()

                    # current row
                    cells = [
                        tree_to_str(reduce_value(io.value_tree, io.reference_tree))
                        for io in sequence.ios
                    ]
                    # tolerance line necessary empty
                    tolerances = ['' for i in range(len(sequence.ios))]
                    # reset comments
                    comments = []
                    cycles = 1
                else:
                    cycles += 1

            flush_line()

        # loop on steps completed: flush the buffered line
        cells = 'fake'
        flush_line(last=True)


def _main(model: Model, scenario_file: str, alias_file: str, output: str) -> int:
    """Entry point for unit tests or reuse."""
    app = Application()
    app.bind(model)
    sequence = Sequence()
    app.add_sequence(sequence)
    sequence.create_scenario(alias_file)
    scenario = sequence.create_scenario(scenario_file)
    if not scenario or not sequence.load():
        print('failed to load alias/scenario files')
        return 1
    out_suffix = Path(output).suffix
    if out_suffix == '.csv':
        save_as_csv(scenario, output)
        return 0
    elif out_suffix == '.sss':
        print('sss output scenarios not supported')
        return 1
    else:
        print('unknown scenario extension', out_suffix)
        return 1


# cf __main__.py
def main(scenario_file: str, alias_file: str, output: str) -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    model = get_sessions()[0].model
    code = _main(model, scenario_file, alias_file, output)
    return code

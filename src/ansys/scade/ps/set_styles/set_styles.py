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
Ansys SCADE Power Scripts: Set equation sets styles.

Reset all the styles of diagrams' equation sets

.. Note::

  * The script can not be executed on the command line.
  * Each equation set is assigned the style ``<prefix><count>`` where
    ``<count>`` starts from 1 and is reset for each diagram, <prefix> is the
    ``PREFIX`` constant defined at the beginning of the script.
  * The <prefix><number> styles are not created.
  * The equation sets are given a default style if the requested one does
    not exist.
"""

import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit

# prefix for styles
PREFIX = 'EQS'


class SetStyle(Visit):
    """Visitor for equation sets."""

    def __init__(self):
        """Visit all loaded models."""
        for session in get_sessions():
            model = session.model
            self.visit(model)

    def visit_net_diagram(self, net_diagram: suite.NetDiagram, *args):
        """Reset the counter before a graphical diagram is visited."""
        self.count = 0
        super().visit_net_diagram(net_diagram, *args)

    def visit_equation_set(self, equation_set: suite.EquationSet, *args):
        """Create or update the style of the visited equation set."""
        self.count += 1
        # suite.set_style is defined dynamically when executed from the SCADE IDE
        suite.set_style(equation_set, '%s%d' % (PREFIX, self.count))  # type: ignore  # reportAttributeAccessIgnore


SetStyle()

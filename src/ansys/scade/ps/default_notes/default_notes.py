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

"""Ansys SCADE Power Scripts: Create default notes for Scade models."""

from enum import Enum

import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
import scade.model.suite.annotation as ann
from scade.model.suite.visitors import Visit

tool = 'Ansys SCADE Power Scripts: Create default notes for Scade models'


class FT(Enum):
    """Annotation attribute type codes."""

    # values obtained by reverse engineering
    INTEGER = 1
    REAL = 2
    BOOLEAN = 3
    CHARACTER = 4
    STRING = 5
    TEXT = 6
    DATE = 8
    ENUM = 9
    FILE = 10


class DefaultNotes(Visit):
    """Creation of default notes for a model."""

    def __init__(self):
        # runtime properties
        self.categories = {}  # type: Dict[str, ann.AnnCategory]
        self.defaults = {}  # type: Dict[ann.AnnAttDefinition, str]

    def build_categories(self, model: suite.Model):
        """Create a map of all categories allowing a faster access."""
        # retrieve the global annotation schema:
        # since it is not directly accessible from the model
        # we need to retrieve it from any note type
        for note_type in model.ann_note_types:
            schema = note_type.annot_schema
            break
        else:
            # no annotation schema: there is nothing to do
            return

        self.categories = {_.name: _ for _ in schema.ann_categories}

    def get_category(self, annotable: suite.Annotable) -> str:
        """Retrieve the category of an annotable element."""
        # default
        category = ''

        if isinstance(annotable, suite.Package) and not isinstance(annotable, suite.Model):
            category = 'package'
        elif isinstance(annotable, suite.Constant):
            category = 'type_element' if annotable.enumeration else 'constant'
        elif isinstance(annotable, suite.LocalVariable):
            if annotable.is_input():
                category = 'input'
            elif annotable.is_output():
                category = 'output'
            elif annotable.is_hidden():
                category = 'hidden'
            elif annotable.is_local() and not annotable.is_internal():
                category = 'probe' if annotable.probe else 'local'
            elif annotable.is_signal():
                category = 'signal'
        elif isinstance(annotable, suite.Sensor):
            category = 'sensor'
        elif isinstance(annotable, suite.NamedType):
            category = 'named_type'
        elif isinstance(annotable, suite.CompositeElement):
            category = 'type_element'
        elif isinstance(annotable, suite.Operator):
            category = 'operator'
        elif isinstance(annotable, suite.Assertion):
            category = 'assertion'
        elif isinstance(annotable, suite.State):
            category = 'state'
        elif isinstance(annotable, suite.StateMachine):
            category = 'state_machine'
        elif isinstance(annotable, suite.Transition):
            category = 'transition'
        elif isinstance(annotable, suite.ActivateBlock):
            category = 'activate_block'
        elif isinstance(annotable, suite.IfNode):
            category = 'branch'
        elif isinstance(annotable, suite.WhenBranch):
            category = 'branch'
        elif isinstance(annotable, suite.Action):
            category = 'action'
        elif isinstance(annotable, suite.Equation):
            if annotable.terminator:
                category = 'terminator'
            else:
                ge = annotable.equation_ge
                if ge and ge.kind == 'OBJ_LIT':
                    category = 'literal'
                else:
                    right = annotable.right
                    if isinstance(right, suite.ExprCall):
                        category = 'ref_operator' if right.operator else 'predef_opr'
                    elif isinstance(right, suite.ExprId):
                        category = 'ref_ident'
        elif isinstance(annotable, suite.EquationSet):
            category = 'equation_set'
        elif isinstance(annotable, suite.NetDiagram):
            category = 'net_diagram'
        elif isinstance(annotable, suite.TextDiagram):
            category = 'text_diagram'
        # documented but meaningless: can't be edited
        # elif isinstance(annotable, suite.TreeDiagram):
        #     category = 'tree_diagram'

        return category

    def compute_default_values(self, model: suite.Model):
        """Update the map of default values for note attributes."""
        for note_type in model.ann_note_types:
            for att in note_type.ann_att_definitions:
                # search for default and enum value properties
                default_property = None
                # # values not accessible for now (25 R1)
                # enum_property = None
                for prop in att.ann_properties:
                    if prop.name == 'NT_DEFAULT_VALUE':
                        default_property = prop
                    # values not accessible for now (25 R1)
                    # elif prop.name == 'NT_ENUM_VALUES':
                    #     enum_property = prop
                # default
                default_value = ''
                ft = FT(att.type)
                if ft == FT.INTEGER:
                    default_value = '0'
                elif ft == FT.REAL:
                    default_value = '0.0'
                elif ft == FT.BOOLEAN:
                    default_value = 'F'
                elif ft == FT.STRING:
                    default_value = ''
                elif ft == FT.TEXT:
                    default_value = ''
                elif ft == FT.CHARACTER:
                    default_value = ' '
                elif ft == FT.DATE:
                    default_value = '01/01/01'
                elif ft == FT.FILE:
                    default_value = ''
                elif ft == FT.ENUM:
                    # values not accessible for now (25 R1)
                    pass

                if default_property:
                    default_value = str(default_property.value)
                    if ft == FT.BOOLEAN:
                        default_value = 'T' if default_value == '1' else 'F'

                self.defaults[att] = default_value

    def create_note(self, annotable: suite.Annotable, note_type: ann.AnnNoteType):
        """Create a default note for an annotable element and a given note type."""
        note = ann.AnnNote(note_type)
        note.ann_note_type = note_type
        note.name = note_type.name
        annotable.ann_notes.append(note)

        for att in note_type.ann_att_definitions:
            ft = FT(att.type)
            if ft == FT.INTEGER:
                cls = ann.AnnAttIntValue
            elif ft == FT.REAL:
                cls = ann.AnnAttRealValue
            elif ft == FT.BOOLEAN:
                cls = ann.AnnAttBoolValue
            elif ft == FT.STRING:
                cls = ann.AnnAttStringValue
            elif ft == FT.TEXT:
                cls = ann.AnnAttStringValue
            elif ft == FT.CHARACTER:
                cls = ann.AnnAttCharValue
            elif ft == FT.DATE:
                cls = ann.AnnAttDateValue
            elif ft == FT.FILE:
                cls = ann.AnnAttFileValue
            elif ft == FT.ENUM:
                cls = ann.AnnAttEnumValue
            else:
                cls = None
            if not cls:
                print(f'unexpected field type {ft.name} for {note_type.name}::{att.name}')
            else:
                default_value = self.defaults[att]
                value = cls(note_type)
                value.ann_att_definition = att
                value.from_string(default_value)
                note.ann_att_values.append(value)

    def visit_annotable(self, annotable: suite.Annotable, *args):
        """Create missing notes of the visited annotable element."""
        # loop on annotabilities
        categories = [self.get_category(annotable)]
        if isinstance(annotable, suite.Operator):
            categories.append(f'ref_{annotable.name}')
        for category in categories:
            ann_category = self.categories.get(category)
            if not ann_category:
                continue
            for annotability in ann_category.annotabilities:
                if not annotability.default_note:
                    continue
                note_type = annotability.ann_note_type
                for note in annotable.ann_notes:
                    if note.ann_note_type == note_type:
                        # note already exists
                        break
                else:
                    # note not found: create one with default values
                    print(f'creating note for {note_type.name}]\n')
                    self.create_note(annotable, note_type)
                    st = annotable.defined_in
                    # root tree diagrams do not have an associated file
                    if st:
                        # the ann file has to be updated
                        st.ann_modified = True
                        # the scade file needs to be saved if the notes are embedded as comments
                        st.sao_modified = True

        # not need to call base function
        # super().visit_annotable(annotable, *args)

    def main(self, session: suite.Session) -> int:
        """Entry point for unit testing or reuse."""
        model = session.model
        self.build_categories(model)
        self.compute_default_values(model)
        # visit all model annotable instances and create missing notes
        self.visit(model)
        # save all modified model and notes files (XSCADE, ANN)
        session.save_model2()
        return 0


def main() -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    return_code = 0
    for session in get_sessions():
        code = DefaultNotes().main(session)
        if code != 0:
            return_code = code

    return return_code

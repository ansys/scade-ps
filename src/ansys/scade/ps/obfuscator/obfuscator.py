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

"""Ansys SCADE Power Scripts: Obfuscator for Scade models."""

from pathlib import Path

# nosec B311  # usage of random is acceptable for obfuscation
# it allows to provide seeds for reproducible unit tests.
import random
from typing import Dict, List, Optional

import scade
import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit

tool = 'Ansys SCADE Power Scripts: Obfuscator for Scade models'


def _get_scade_path(object_: suite.Object) -> str:
    """Return a path for objects for which get_full_path is not enough."""
    if isinstance(object_, suite.CompositeElement):
        # structure's field
        return object_.owner.get_full_path() + object_.name
    elif isinstance(object_, suite.Diagram):
        return object_.owner.get_full_path() + object_.name
    elif isinstance(object_, suite.EquationSet):
        return _get_scade_path(object_.owner) + '/' + object_.name
    else:
        return object_.get_full_path()


class _State:
    """Global variables for the obfuscation process."""

    def __init__(self):
        # dictionary old name to new name
        self.names = {}  # type: Dict[str, str]
        # dictionary object to old path
        self.old_names = {}  # type: Dict[suite.Object, str]
        # dictionary object to new path
        self.new_names = {}  # type: Dict[suite.Object, str]
        # modified storage units
        self.units = []  # type: List[suite.StorageUnit]
        # dictionary old file name to new file name
        self.files = {}  # type: Dict[str, str]


class _FilteredVisit(Visit):
    """Base visitor for caching and renaming items."""

    def __init__(self, state: _State, rename_internals: bool, ignored_libraries: List[str]):
        self.state = state
        self.libraries = set(ignored_libraries)
        self.rename_internals = rename_internals

    def visit(self, item):
        """Redefinition to consider instances of Session."""
        if isinstance(item, suite.Session):
            # visit all loaded models
            for model in item.loaded_models:
                super().visit(model)
        else:
            super().visit(item)

    def visit_object(self, object_: suite.Object, *args):
        """Call ``on_named`` if the visited object has a name."""
        if hasattr(object_, 'name') and object_.name:
            # process the named object
            self.on_named(object_)

    def visit_local_variable(self, local_variable: suite.LocalVariable, *args):
        """Filter internal variables depending on the options."""
        if not local_variable.is_internal() or self.rename_internals:
            super().visit_local_variable(local_variable, *args)
        # else: skip internal variables

    def on_named(self, named: suite.Object):
        """Process a named object."""
        pass


class _Cache(_FilteredVisit):
    """Visitor to cache the objects' path before they are renamed."""

    def on_named(self, named: suite.Object):
        """Process a named object."""
        if isinstance(named, suite.Model):
            self.state.old_names[named] = named.name
        else:
            self.state.old_names[named] = _get_scade_path(named)

    def visit_model(self, model: suite.Model, *args):
        """Filter the libraries that should be ignored."""
        if model.name not in self.libraries:
            super().visit_model(model, *args)


class _Rename(_FilteredVisit):
    """Visitor to rename objects and files."""

    def get_name(self, old_name: str) -> str:
        """
        Create a new name: pattern XXX999, random characters and digits.

        The mapping is stored in a dictionary, to make sure there
        is only one new name for an existing one.
        """
        name = self.state.names.get(old_name, '')
        while not name:
            name = ''.join(
                ['%c' % (65 + random.randrange(0, 26)) for _ in range(3)]  # nosec B311
                + ['%c' % (48 + random.randrange(0, 10)) for _ in range(3)]  # nosec B311
            )
            # check uniqueness
            if name in self.state.names:
                # unlikely but who knows?
                # same player shoot again
                name = ''
            else:
                if old_name and old_name[0] == "'":
                    # polymorphic type
                    name = "'" + name
                self.state.names[old_name] = name

        return name

    def on_named(self, named: suite.Object):
        """Process a named object."""
        named.name = self.get_name(named.name)
        if isinstance(named, suite.Model):
            self.state.new_names[named] = named.name
        else:
            # name of owning objects already changed
            self.state.new_names[named] = _get_scade_path(named)

    def visit_const_value(self, const_value: suite.ConstValue, *args):
        """Rename the expression's label if any."""
        if const_value.kind == 'Label':
            # label for projections
            const_value.value = self.get_name(const_value.value)
        super().visit_const_value(const_value, *args)

    def visit_storage_unit(self, storage_unit: suite.StorageUnit, *args):
        """Delete the referenced files and mark them as modified."""

        def with_stem(path: Path, name: str) -> Path:
            """Implement Path.with_stem for Python 3.7."""
            return path.with_name(name + path.suffix)

        path_sao = Path(storage_unit.sao_file_name)
        new_name = self.get_name(path_sao.stem)
        if path_sao.exists():
            path_sao.unlink()
            storage_unit.sao_modified = True
        path_ann = Path(storage_unit.ann_file_name)
        if path_ann.exists():
            # for some reason, it is not possible to save the annotation files
            # - StorageUnit.save does not save annotation files
            # - Session.save_model2 does not save libraries
            # so rename the annotation files since they are not modified
            path_ann.rename(with_stem(path_ann, new_name))
        self.state.units.append(storage_unit)
        # path of the file
        storage_unit.sao_file_name = str(with_stem(path_sao, new_name))
        storage_unit.ann_file_name = str(with_stem(path_ann, new_name))
        # reference of the file
        persist_as = Path(storage_unit.persist_as)
        new_persist_as = with_stem(persist_as, new_name)
        storage_unit.persist_as = str(new_persist_as)
        # record the name change
        suffix = path_sao.suffix
        self.state.files[persist_as.with_suffix(suffix).name] = new_persist_as.with_suffix(
            suffix
        ).name
        super().visit_storage_unit(storage_unit, *args)

    def visit_presentation_element(self, presentation_element: suite.PresentationElement, *args):
        """Remove formatting, if any."""
        presentation_element.text_areas = []
        super().visit_presentation_element(presentation_element, *args)

    def visit_text_diagram(self, text_diagram: suite.TextDiagram, *args):
        """Remove formatting, if any."""
        # None is a legal value to remove an association
        text_diagram.text_area = None  # type: ignore
        super().visit_text_diagram(text_diagram, *args)

    def visit_model(self, model: suite.Model, *args):
        """Rename the items of a model if it is not excluded."""
        if model.name not in self.libraries:
            # initialize an entry for the model and
            # register the name change for the project file
            new_name = self.get_name(model.name)
            self.state.files[model.name + '.etp'] = new_name + '.etp'
            super().visit_model(model, *args)
        else:
            # register the storage units for saving only
            self.state.units += model.model_storage_units


class Obfuscator:
    """Obfuscation of a model."""

    def __init__(
        self, trace_file: str, rename_internals: bool, ignored_libraries: List[str], seed: str
    ):
        # options
        self.trace_file = trace_file
        self.rename_internals = rename_internals
        self.ignored_libraries = ignored_libraries
        if seed:
            random.seed(seed)
        # runtime caches
        self.state = _State()

    def update_projects(self, session: suite.Session):
        """Propagate the filename changes for each project."""
        # two passes to avoid computing the project's dependencies
        projects = []
        # first pass to update the file references
        for model in session.loaded_models:
            path = Path(model.descriptor.model_file_name)
            # scade is a CPython module defined dynamically
            # scade is a CPython module defined dynamically
            project = scade.load_project(str(path))  # type: ignore
            # referenced files
            for file_ref in project.file_refs:
                path_file = Path(file_ref.pathname)
                new_name = self.state.files.get(path_file.name)
                if new_name:
                    file_ref.set_path_name(str(path_file.with_name(new_name)))
            # project
            if path.stem in self.ignored_libraries:
                # project not renamed but might reference renamed files
                project.save(str(path))
            else:
                new_name = self.state.files.get(path.name, path.name)
                projects.append((project, path.with_name(new_name)))
        # second pass to save the renamed projects
        for project, path in projects:
            path_project = Path(project.pathname)
            if path_project.exists():
                # missing_ok not available Python 3.7
                path_project.unlink()
            project.save(str(path))

    def dump_traceability(self, f, src: Dict[suite.Object, str], dst: Dict[suite.Object, str]):
        """Report the tracebility between old names and new names."""
        keys = sorted([(key, value) for key, value in src.items()], key=lambda _: _[1])
        for key, name in keys:
            f.write('%s\t%s\n' % (name, dst[key]))

    def main(self, session: suite.Session) -> int:
        """Entry point for unit testing or reuse."""
        # cache all objects with old names
        self.cache_items(session)
        # rename all objects
        self.rename_items(session)
        # save the units
        for unit in self.state.units:
            unit.save()
        # update the projects
        self.update_projects(session)
        # dump mapping
        if self.trace_file:
            with Path(self.trace_file).open('w') as f:
                f.write('- old names to new names\n')
                self.dump_traceability(f, self.state.old_names, self.state.new_names)
                f.write('- new names to old names\n')
                self.dump_traceability(f, self.state.new_names, self.state.old_names)

        print('command completed')
        return 0

    def cache_items(self, session):
        """Return the dictionary object to scade path before the renamings."""
        visitor = _Cache(self.state, self.rename_internals, self.ignored_libraries)
        visitor.visit(session)

    def rename_items(self, session):
        """Rename the loaded models and return the dictionary object to scade path."""
        visitor = _Rename(self.state, self.rename_internals, self.ignored_libraries)
        visitor.visit(session)


def main(
    trace_file: str = '',
    rename_internals: bool = False,
    ignored_libraries: Optional[List[str]] = None,
    seed: str = '',
) -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    session = get_sessions()[0]
    if ignored_libraries is None:
        ignored_libraries = []
    code = Obfuscator(trace_file, rename_internals, ignored_libraries, seed).main(session)
    return code

Default notes
#############

Rationale
=========

SCADE Suite supports the creation of notes on model elements. Notes are structured data that supplement
the model. They may sometimes be propagated to generated code.

The policy for creating notes is governed by a ``.aty`` configuration file. This file may include
instructions to automatically create default notes whenever new model elements are created. However,
if this policy is defined / modified for an already-existing project, SCADE does not retroactively
create notes for pre-existing model elements.

.. Note::

   For more information on notes and ``.aty`` files, please refer to *Annotation Type Files* in
   section 1 of the *SCADE Suite Technical Manual - Editor*, available
   on `Ansys Help <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/prod_page.html?pn=SCADE&pid=SCADE&lang=en>`_.

Description
===========

This tool creates default notes for a SCADE Suite model.

It considers the annotability rules of the annotation type files (``.aty``)
specified for a project to create the missing default notes for model elements.

* Default notes are identified by the property ``default_note_boolean``
* The cardinality properties ``min_card`` and ``max_card`` are ignored

Usage
=====

.. code:: text

   usage: ansys_scade_ps_default_notes [-h] -p <project> [<project> ...]

   Ansys SCADE Power Scripts: Create default notes for Scade models

   options:
     -h, --help            show this help message and exit
     -p <project> [<project> ...], --projects <project> [<project> ...]
                           SCADE Suite projects

Limitations
===========

* The script does not add missing fields of existing annotations
* The script does not remove obsolete annotations/fields

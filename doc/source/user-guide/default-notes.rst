Default notes
#############

Description
===========

This tool creates default notes for a SCADE Suite model.

It considers the annotability rules of the annotation type files (ATY)
specified for a project to create the missing default notes for the model elements.

* Default notes are identified by the property ``default_note_boolean``
* The cardinality properties ``min_card`` and ``max_card`` are ignored.

Refer to *Annotation Type Files (ATY)* in section 1 of the *SCADE Suite Technical Manual - Editor*
in the SCADE Suite documentation for a complete reference on annotation type files.

Usage
=====

.. code:: bash

   usage: ansys_scade_ps_default_notes [-h] [-p <projects> [<projects> ...]]

   Ansys SCADE Power Scripts: Create default notes for Scade models

   options:
     -h, --help            show this help message and exit
     -p <project> [<project> ...], --projects <project> [<project> ...]
                           SCADE Suite projects

Limitations
===========

* The script does not add missing fields of existing annotations
* The script does not remove obsolete annotations/fields

Rename unused files
###################

Rationale
=========

When renaming model elements, SCADE may sometimes create new files. For instance,
if the "Filename" property of an operator is modified, SCADE will generate
a new ``.xscade`` file with the new name for the operator.

For safety reasons, old files are not removed in such cases, as other projects
may reference them. Over time, this means a SCADE project may become encumbered
with obsolete files.

.. Note::
Two IDE settings may be used when working with SCADE models:
* *Tools > Settings > General > Use a creation dialog box*: prompts for an element and
  file name upon creation of operators and packages.
* *Tools > Settings > General > Propagate entity name changes to filename*: automatically
  creates a new file, as required, upon renaming of a model element.

Description
===========

This tool identifies the model files that are not referenced in a SCADE Suite
project, for example after the renaming of an operator or a package.

The unused files are renamed with a suffix ``.toremove``. This allows you to
double-check the list of unused files, and then delete them easily from the
command line or the Windows explorer.

This tool considers SCADE model files (XSCADE, SCADE) and annotation files (ANN).

Usage
=====

.. code:: text

   usage: ansys_scade_ps_rename_unused [-h] -p <project> [<project> ...]

   Ansys SCADE Power Scripts: Rename unused files

   options:
     -h, --help            show this help message and exit
     -p <project> [<project> ...], --projects <project> [<project> ...]
                           SCADE Suite projects

Limitations
===========

* The symbol files are not considered

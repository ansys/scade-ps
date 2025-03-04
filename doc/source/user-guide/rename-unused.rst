Rename unused files
###################

Description
===========

This tool identifies the model files that are not referenced in a SCADE Suite
project, for example after the renaming of an operator or a package.

The unused files are renamed with a suffix ``.toremove``. This allows you to
double-check the list of unused files, and then delete them easily from the
command line or the Windows explorer.

This too considers SCADE model files (XSCADE, SCADE) and annotation files (ANN).

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

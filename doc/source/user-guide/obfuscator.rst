Obfuscator
##########

Description
===========

This tool obfuscates a SCADE Suite model and its libraries.

* All the names are obfuscated
* The files are renamed, and the old ones are deleted
* The script produces traceability matrices for both objects and file names

.. Note::

   * The model and its libraries are modified in place: **copy
     your files** to another directory before proceeding.
   * Make sure your model does not refer to a library that is not part of your project,
     such as ``$(SCADE)/libraries/libdigital.etp``, or use the option ``-l`` to
     exclude it from the obfuscation process. for example: ``-l libdigital``.

Usage
=====

.. code:: bash

   usage: ansys_scade_power_scripts_obfuscator [-h] -p <project> [-t <trace>] [-i] [-l [library ...]]

   Ansys SCADE Power Scripts: Obfuscator for Scade models

   options:
     -h, --help            show this help message and exit
     -p <project>, --project <project>
                           SCADE Suite project
     -t <trace>, --trace <trace>
                           Output trace file
     -i, --internals       Rename internal variables
     -l [library ...], --ignored_libraries [library ...]
                           Ignored libraries

Limitations
===========

* Project properties are unchanged: root, expanded, instrumented operators...
* KCG pragma name are unchanged
* Imported code is unchanged
* Project files accessed with an absolute path are modified
* Symbol files (SSL) are not taken into account
* Projects with files with same names in different directories are not supported

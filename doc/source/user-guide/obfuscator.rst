Obfuscator
##########

Rationale
=========

SCADE Suite models sometimes need to be shared with partners. Example use cases include developing
operator libraries for a higher-level model, or trying to reproduce a specific behavior using two
connected models developed by different teams at different companies.

The model being shared may sometimes contain sensitive intellectual property. Obfuscation is often
seen as an acceptable compromise to protect this IP while still sharing the model.

Description
===========

This tool obfuscates a SCADE Suite model and its libraries.

* All names are obfuscated
* Files are renamed and the old ones are deleted
* The script produces traceability matrices for both objects and file names

.. Note::

   * The model and its libraries are modified in place: **copy
     your files** to another directory before proceeding.
   * Make sure your model does not refer to a library that is not part of your project,
     such as ``$(SCADE)/libraries/libdigital.etp``, or use the option ``-l`` to
     exclude it from the obfuscation process. for example: ``-l libdigital``.

Usage
=====

.. code:: text

   usage: ansys_scade_ps_obfuscator [-h] -p <project> [-t <trace>] [-i] [-l [library ...]] [-s <seed>]

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
     -s <seed>, --seed <seed>
                           Random seed for obfuscation

For example:

.. code:: bash

   ansys_scade_ps_obfuscator -p MyProject.etp -t Mapping.txt -l libdigital libmath

This command obfuscates ``MyProject.etp`` and its libraries except those named ``libdigital`` or ``libmath``.

The traceability information between old and new names is output to ``Mapping.txt``, as follows:

.. code:: text

   Behavior::	BGK375::
   Behavior::Impl::	BGK375::UBJ269::
   Behavior::Impl::Iter/	BGK375::UBJ269::YOM827/
   Behavior::Impl::Iter/'T/	BGK375::UBJ269::YOM827/'FOP322/
   Behavior::Impl::Iter/Iter	BGK375::UBJ269::YOM827/YOM827
   ...

Limitations
===========

* Project properties are unchanged: root, expanded, instrumented operators, etc.
* KCG ``pragma name`` are unchanged.
* Imported code is unchanged.
* Project files accessed with an absolute path are modified.
* Symbol files (SSL) are not taken into account.
* Projects with files with same names in different directories are not supported.
* Homonymy is preserved: model elements with the same name, for example an operator
  and its diagram, have the same obfuscated name.

User Guide
##########

Launch
======

The command-line tools contained in this package can be launched in two different ways:
executable or Python module.

Executable
----------

The binaries are in the ``Scripts`` directory of your Python environment.
Either add this directory to ``PATH`` or use an absolute path.

.. code:: bash

    ansys_scade_power_scripts_<tool> <arg>*

Where ``<tool>`` is the name of the tool to run.

For example:

.. code:: bash

   ansys_scade_power_scripts_obfuscator -p my_project.etp -i -t trace.txt

Python module
-------------

.. code:: bash

    python -m ansys.scade.ps.<tool> <arg>*

Where ``<tool>`` is the name of the tool to run.

For example:

.. code:: bash

   python -m ansys.scade.ps.obfuscator -p my_project.etp -i -t trace.txt

SCADE Release
=============

The tools rely on `Ansys SCADE API Tools`_ to select the version of SCADE to use at runtime.
Refer to `Advanced usage with API tools`_ for details or if you want to select a
given release of SCADE.

Tools
=====

.. toctree::
   :maxdepth: 1

   obfuscator

.. LINKS AND REFERENCES

.. _Ansys SCADE API Tools: https://apitools.scade.docs.pyansys.com/version/stable/index.html
.. _Advanced usage with API tools: https://apitools.scade.docs.pyansys.com/version/stable/user_guide/scripting.html#advanced-usage-with-api-tools

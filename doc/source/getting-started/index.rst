Getting started
###############
To use Ansys SCADE Power Scripts, you must have a valid license for Ansys SCADE.

For information on getting a licensed copy, see the
`Ansys SCADE Suite <https://www.ansys.com/products/embedded-software/ansys-scade-suite>`_
page on the Ansys website.

Requirements
============
The ``ansys-scade-ps`` package supports only the versions of Python delivered with
Ansys SCADE, starting from 2021 R2:

* 2021 R2 to 2023 R1: Python 3.7
* 2023 R2 through 2025 R2: Python 3.10
* 2026 R1 and later: Python 3.12

.. _install-user-mode:

Install in user mode
====================
The following steps are for installing Ansys SCADE Power Scripts in user mode. If you want to
contribute to Ansys SCADE Power Scripts,
see :ref:`contribute_scade_ps` to install in developer mode.

#. Before installing Ansys SCADE Power Scripts in user mode, run this command to ensure that
   you have the latest version of `pip`_:

   .. code:: bash

      python -m pip install -U pip

#. Install Ansys SCADE Power Scripts with this command:

   .. code:: bash

       python -m pip install ansys-scade-ps

.. _run-tools:

Run the tools
=============

The command-line tools contained in this package can be launched in two different ways:
executable or Python module.

They rely on `Ansys SCADE API Tools`_ to select the version of SCADE to use at runtime.
Refer to `Advanced usage with API tools`_ for details or if you want to select a
specific release of SCADE.

Executable
----------

The binaries are in the ``Scripts`` directory of your Python environment.
Either add this directory to ``PATH`` or use an absolute path.

.. code:: bash

    ansys_scade_ps_<tool> <arg>*

Where ``<tool>`` is the name of the tool to run.

For example:

.. code:: bash

   ansys_scade_ps_obfuscator -p my_project.etp -i -t trace.txt

Python module
-------------

.. code:: bash

    python -m ansys.scade.ps.<tool> <arg>*

Where ``<tool>`` is the name of the tool to run.

For example:

.. code:: bash

   python -m ansys.scade.ps.obfuscator -p my_project.etp -i -t trace.txt

.. LINKS AND REFERENCES
.. _pip: https://pypi.org/project/pip/
.. _Ansys SCADE API Tools: https://apitools.scade.docs.pyansys.com/version/stable/index.html
.. _Advanced usage with API tools: https://apitools.scade.docs.pyansys.com/version/stable/user_guide/scripting.html#advanced-usage-with-api-tools

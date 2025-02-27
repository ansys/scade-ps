Getting started
===============
To use Ansys SCADE Power Scripts, you must have a valid license for Ansys SCADE.

For information on getting a licensed copy, see the
`Ansys SCADE Suite <https://www.ansys.com/products/embedded-software/ansys-scade-suite>`_
page on the Ansys website.

Requirements
------------
The ``ansys-scade-ps`` package supports only the versions of Python delivered with
Ansys SCADE, starting from 2021 R2:

* 2021 R2 to 2023 R1: Python 3.7
* 2023 R2 and later: Python 3.10

.. _install-user-mode:

Install in user mode
--------------------
The following steps are for installing Ansys SCADE Power Scripts in user mode. If you want to
contribute to Ansys SCADE Power Scripts,
see :ref:`contribute_scade_ps` for installing in developer mode.

#. Before installing Ansys SCADE Power Scripts in user mode, run this command to ensure that
   you have the latest version of `pip`_:

   .. code:: bash

      python -m pip install -U pip

#. Install Ansys SCADE Power Scripts with this command:

   .. code:: bash

       python -m pip install ansys-scade-ps

.. LINKS AND REFERENCES
.. _pip: https://pypi.org/project/pip/

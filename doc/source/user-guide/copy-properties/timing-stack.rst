Timing and Stack Analysis Tools
###############################

Template: ``timing_stack_analysis_tools.json``.

.. vale off

General
=======

.. image:: /_static/tsat_general.png

Tool: ``a3``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Session Name
     - SESSION_NAME
     - `$(Configuration)`
     -
   * - aiT version
     - VERSION
     -
     -
   * - aiT binary folder
     - AIT_BINDIR
     -
     -
   * - Type
     - CPU
     -
     -
   * - Basic clock
     - BASIC_CLOCK
     - `-1`
     -
   * - Unit
     - UNIT
     - `Hz`
     -
   * - User ais file
     - AIS_FILE
     -
     -

Advanced Verifier Usage
=======================

.. image:: /_static/tsat_advanced_verifier_usage.png

Tool: ``a3``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Interactive
     - INTERACTIVE
     - `false`
     -
   * - Max unroll
     - MAX_UNROLL
     - `2`
     -
   * - Default unroll
     - DEFAULT_UNROLL
     - `2`
     -
   * - External environment file
     - XTC_FILE
     -
     -

Imported Operators
==================

.. image:: /_static/tsat_imported_operators.png

Tool: ``a3``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * -
     - SPECIFIED_OPERATORS
     -
     - list of strings `<scade path>|<cycles>-<bytes>`
   * -
     - EXTERNAL_FUNCTIONS
     -
     - list of strings `<name>:<cycles>-<bytes>`

.. vale on

Test Tool
#########

Template: ``test_tool.json``.

.. vale off

General
=======

.. image:: /_static/tt_general.png

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Process the following procedures
     - USE_PROCEDURES_LIST
     - `false`
     -
   * -
     - PROCEDURES_LIST_SELECTION_MODE
     - `1`
     - `0` (All), `1` (Selected), `2` (All except selected)
   * -
     - SELECTED_PROCEDURES
     -
     - list of procedures
   * -
     - NOT_SELECTED_PROCEDURES
     -
     - list of procedures

Host Execution
==============

.. image:: /_static/tt_host_execution.png

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Source configuration
     - TEE_CONF
     -
     -
   * - Target directory
     - TEE_TARGET_DIR
     - `$(Configuration)_TEE`
     -
   * - No build
     - TEE_NO_BUILD
     - `false`
     -
   * - Report details
     - TEE_DETAILS_FAILED
     - `false`
     -

Model Coverage
==============

.. image:: /_static/tt_model_coverage.png

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Source configuration
     - MC_CONF
     -
     -
   * - Target directory
     - MC_TARGET_DIR
     - `$(Configuration)_MC`
     -
   * - Coverage criterion
     - MC_COVERAGE_CRITERION
     - `ODC`
     - `influence`, `ODC`, `OMCDC`
   * - No build
     - MC_NO_BUILD
     - `false`
     -
   * - Generate DO-331 FAQ#11 log
     - MC_FAQ11
     - `true`
     -
   * - Coverage results
     - MC_MERGE_PREV_RESULTS
     - `true`
     -
   * - Select operators
     - MC_INSTRUMENTATION_MODE
     - `1`
     - `0` (All), `1` (Selected), `2` (All except selected)
   * -
     - MC_INSTRUMENTED_NODES
     -
     - list of scade paths
   * -
     - MC_NOT_INSTRUMENTED_NODES
     -
     - list of scade paths
   * - Additional points
     - MC_OBSERVER_LIBS
     -
     - list of files

Coverability Analysis
=====================

.. image:: /_static/tt_coverability_analysis.png

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Timeout (seconds)
     - DV_MC_TIMEOUT
     - `120`
     -
   * - Maximum scenario length
     - DV_MC_BMC_DEPTH
     - `4`
     -
   * - Number of threads
     - DV_MC_THREADS
     - `4`
     -
   * - Custom strategy
     - DV_MC_STRATEGY
     -
     -
   * - Allow subnormal values
     - DV_MC_FPSUBVALUES
     - `false`
     -
   * - Generate oracles
     - DV_MC_ORACLE_GENERATION
     - `false`
     -
   * - Relative tolerance
     - DV_MC_TCGEN_TOOL
     - `0.01`
     -
   * - Set only relevant inputs
     - DV_MC_DONTCARES_REMOVAL
     - `false`
     -
   * - Abstraction operators
     - DV_MC_ABSTRACTION_LIBS
     -
     -
   * - Include justified points in analysis
     - DV_MC_ANALYZE_NO_J
     - `false`
     -

Harness Generation
==================

.. image:: /_static/tt_harness_generation.png

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Source configuration
     - THG_CONF
     -
     -
   * - Source configuration
     - THG_TARGET_DIR
     - `$(Configuration)_THG`
     -
   * - Target test environment
     - TARGET
     - `TBRUN`
     - `TBRUN`, `RTRT`, `VCAST`, `<CUSTOM ID>`...

LDRA Test Suite
===============

.. image:: /_static/tt_ldra_test_suite.png

Tool: ``TBRUN``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - User initialization function
     - USER_INIT
     -
     -

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * -
     - TARGET_TBRUN
     -
     - summary command-line split as list of tokens: `[-user_init <USER_INIT>]`

RTRT
====

.. image:: /_static/tt_rtrt.png

Tool: ``RTRT``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Generate C89-based harnesses
     - C89
     - `false`
     -
   * - User initialization function
     - USER_INIT
     -
     -

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * -
     - TARGET_RTRT
     -
     - summary command-line split as list of tokens: `[-c89] [-user_init <USER_INIT>]`

VectorCAST
==========

.. image:: /_static/tt_vector_cast.png

Tool: ``VCAST``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Sensor unit name
     - SENSOR_UNIT
     -
     -
   * - Split by scenario
     - SPLIT
     - `false`
     -
   * - Max line length
     - LINE_LENGTH
     - 0
     -
   * - User initialization function
     - USER_INIT
     -
     -

Tool: ``QTE``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * -
     - TARGET_VCAST
     -
     - summary command-line split as list of tokens: `[-sensort_unit <SENSOR_UNIT>] [-split] [-max_line_length <LINE_LENGTH>] [-user_init <USER_INIT>]`

.. vale on

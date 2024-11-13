#
# Copyright 2024 ...
#
# SPDX-License-Identifier: Apache-2.0
r"""
==============================
B666: Test for the use of a big bad wolf
==============================

This plugin test checks for the use of Python variable, method, or keyword called `big_bad_wolf`.

:Example:

.. code-block:: none

    >> Issue: Use of big_bad_wolf detected.
       Severity: Medium   Confidence: High
       CWE: CWE-00 (https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
       Location: ./examples/big_bad_wolf.py:1
    1 big_bad_wolf = 1


.. seealso::

 - https://docs.python.org/

.. versionadded:: 1.7.10

.. versionchanged:: 1.7.10

"""
import bandit
from bandit.core import issue
from bandit.core import test_properties as test


def big_bad_wolf_issue():
    return bandit.Issue(
        severity=bandit.MEDIUM,
        confidence=bandit.HIGH,
        cwe=issue.Cwe.NOTSET,
        text="Big bad wolf detected. Get out of here now.",
    )


@test.checks("Call")
@test.test_id("B666")
def big_bad_wolf_used(context):
    if "big_bad_wolf" in context.call_function_name_qual:
        return big_bad_wolf_issue()

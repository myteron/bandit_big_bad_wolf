#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# SPDX-License-Identifier: Apache-2.0
import os

import testtools

from bandit.core import config as b_config
from bandit.core import constants as C
from bandit.core import manager as b_manager
from bandit.core import metrics
from bandit.core import test_set as b_test_set

# we want debug mode to be on
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class FunctionalTests(testtools.TestCase):
    """Functional tests for bandit test plugins.

    This set of tests runs bandit against each example file in turn
    and records the score returned. This is compared to a known good value.
    When new tests are added to an example the expected result should be
    adjusted to match.
    """

    def setUp(self):
        super().setUp()
        # NOTE(tkelsey): bandit is very sensitive to paths, so stitch
        # them up here for the testing environment.
        #
        # TODO: change "bandit_big_bad_wolf" to match module name
        path = os.path.join(os.getcwd(), "bandit_big_bad_wolf")
        b_conf = b_config.BanditConfig()
        self.b_mgr = b_manager.BanditManager(b_conf, "file")
        self.b_mgr.b_conf._settings["plugins_dir"] = path
        self.b_mgr.b_ts = b_test_set.BanditTestSet(config=b_conf)

    def run_example(self, example_script, ignore_nosec=False):
        """A helper method to run the specified test

        This method runs the test, which populates the self.b_mgr.scores
        value. Call this directly if you need to run a test, but do not
        need to test the resulting scores against specified values.
        :param example_script: Filename of an example script to test
        """
        path = os.path.join(os.getcwd(), "examples", example_script)
        self.b_mgr.ignore_nosec = ignore_nosec
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()

    def check_example(self, example_script, expect, ignore_nosec=False):
        """A helper method to test the scores for example scripts.

        :param example_script: Filename of an example script to test
        :param expect: dict with expected counts of issue types
        """
        # reset scores for subsequent calls to check_example
        self.b_mgr.scores = []
        self.run_example(example_script, ignore_nosec=ignore_nosec)

        result = {
            "SEVERITY": {"UNDEFINED": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "CONFIDENCE": {"UNDEFINED": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0},
        }

        for test_scores in self.b_mgr.scores:
            for score_type in test_scores:
                self.assertIn(score_type, expect)
                for idx, rank in enumerate(C.RANKING):
                    result[score_type][rank] = (
                        test_scores[score_type][idx] // C.RANKING_VALUES[rank]
                    )

        self.assertDictEqual(expect, result)

    def check_metrics(self, example_script, expect):
        """A helper method to test the metrics being returned.

        :param example_script: Filename of an example script to test
        :param expect: dict with expected values of metrics
        """
        self.b_mgr.metrics = metrics.Metrics()
        self.b_mgr.scores = []
        self.run_example(example_script)

        # test general metrics (excludes issue counts)
        m = self.b_mgr.metrics.data
        for k in expect:
            if k != "issues":
                self.assertEqual(expect[k], m["_totals"][k])
        # test issue counts
        if "issues" in expect:
            for criteria, _ in C.CRITERIA:
                for rank in C.RANKING:
                    label = f"{criteria}.{rank}"
                    expected = 0
                    if expect["issues"].get(criteria).get(rank):
                        expected = expect["issues"][criteria][rank]
                    self.assertEqual(expected, m["_totals"][label])

    def test_big_bad_wolf(self):
        """Lets see if we can detect a big bad wolf"""
        # TODO: change expect to match rating in the vulnerabilty detection file
        expect = {
            "SEVERITY": {"UNDEFINED": 0, "LOW": 0, "MEDIUM": 1, "HIGH": 0},
            "CONFIDENCE": {"UNDEFINED": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 1},
        }
        self.check_example("big_bad_wolf.py", expect)

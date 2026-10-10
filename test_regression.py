
import unittest

from regression import compare_regressions


class TestRegressionComparison(unittest.TestCase):

    def test_new_failure(self):
        baseline = "INFO: Simulation started"
        current = "ERROR: Packet transmission failed"

        result = compare_regressions(baseline, current)

        self.assertGreater(
            len(result["new_failures"]), 0
        )

    def test_resolved_failure(self):
        baseline = "ERROR: Packet transmission failed"
        current = "INFO: Simulation passed"

        result = compare_regressions(baseline, current)

        self.assertGreater(
            len(result["resolved_failures"]), 0
        )

    def test_recurring_failure(self):
        baseline = "ERROR: Packet transmission failed"
        current = "ERROR: Packet transmission failed"

        result = compare_regressions(baseline, current)

        self.assertGreater(
            len(result["recurring_failures"]), 0
        )


if __name__ == "__main__":
    unittest.main()

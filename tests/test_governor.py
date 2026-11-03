"""Unit tests for CostGovernor."""
import unittest
from agent_cost_governor.governor import CostGovernor, BudgetExceededError

class TestCostGovernor(unittest.TestCase):
    def test_soft_limit_degradation(self):
        gov = CostGovernor(max_budget_usd=1.00, soft_limit_ratio=0.50)
        self.assertEqual(gov.recommend_model("gemini-pro"), "gemini-pro")
        gov.current_spend = 0.60
        self.assertEqual(gov.recommend_model("gemini-pro"), "gemini-flash")

    def test_hard_limit_exception(self):
        gov = CostGovernor(max_budget_usd=0.10)
        with self.assertRaises(BudgetExceededError):
            gov.record_usage("gemini-pro", 10_000, 50_000)

if __name__ == "__main__":
    unittest.main()

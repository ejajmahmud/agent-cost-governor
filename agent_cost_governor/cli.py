"""Command-line interface for Agent Cost Governor."""
import argparse
from .governor import CostGovernor, BudgetExceededError

def main():
    parser = argparse.ArgumentParser(description="Agent Cost Governor CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate cost tracking and degradation")
    args = parser.parse_args()

    gov = CostGovernor(max_budget_usd=1.00, soft_limit_ratio=0.50)
    print("Initial recommended model:", gov.recommend_model("gemini-pro"))

    # Record 100,000 output tokens on pro (~$0.50)
    gov.record_usage("gemini-pro", input_tokens=10_000, output_tokens=100_000)
    print("Spend after heavy query:", gov.stats())
    print("Recommended model after soft limit reached:", gov.recommend_model("gemini-pro"))

if __name__ == "__main__":
    main()

"""Real-time financial budget tracking and model degradation governor."""
from typing import Dict, Any, Tuple


class BudgetExceededError(RuntimeError):
    pass


class CostGovernor:
    PRICING = {
        "gemini-pro": {"input": 1.25 / 1_000_000, "output": 5.00 / 1_000_000},
        "gemini-flash": {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
    }

    def __init__(self, max_budget_usd: float = 10.0, soft_limit_ratio: float = 0.75):
        self.max_budget = max_budget_usd
        self.soft_limit = max_budget_usd * soft_limit_ratio
        self.current_spend = 0.0

    def record_usage(self, model: str, input_tokens: int, output_tokens: int) -> float:
        rates = self.PRICING.get(model, self.PRICING["gemini-flash"])
        cost = (input_tokens * rates["input"]) + (output_tokens * rates["output"])
        self.current_spend += cost

        if self.current_spend >= self.max_budget:
            raise BudgetExceededError(f"Hard budget limit of ${self.max_budget:.2f} exceeded! Current spend: ${self.current_spend:.4f}")

        return round(cost, 6)

    def recommend_model(self, preferred_model: str) -> str:
        """Degrades to cheap model if spend passes soft limit."""
        if self.current_spend >= self.soft_limit:
            return "gemini-flash"
        return preferred_model

    def stats(self) -> Dict[str, Any]:
        return {
            "spent_usd": round(self.current_spend, 4),
            "budget_usd": self.max_budget,
            "utilization_pct": round((self.current_spend / self.max_budget) * 100, 2),
            "soft_limit_reached": self.current_spend >= self.soft_limit
        }

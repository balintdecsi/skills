"""Back-of-envelope market sizing and unit economics for an early-stage product.

Standard library only, so it runs anywhere (`python unit_economics.py` or `uv run`).
Copy it into the product repo, replace the example inputs with sourced numbers, and keep the
output next to the assumptions it depends on (e.g. docs/discovery/market_sizing.md).

Conventions:
- Money is in one currency per run (the default label is EUR).
- LTV is gross-margin profit over a fixed horizon (default 5 years, as in Aulet's
  *Disciplined Entrepreneurship*), with survival decaying by churn and each year discounted
  at the cost of capital: profit_t / (1 + r) ** t.
- CAC includes *all* sales and marketing spend in the period, including failed campaigns
  and an imputed cost for founder time, divided by customers actually won.
"""

from __future__ import annotations

from dataclasses import dataclass


def bottom_up_tam(customers: int, annual_revenue_per_customer: float) -> float:
    """Number of customers matching the end-user profile × yearly spend per customer."""
    return customers * annual_revenue_per_customer


def top_down_tam(market_size: float, share_matching_profile: float) -> float:
    """Industry-report market size × share of it that fits the end-user profile (0–1)."""
    return market_size * share_matching_profile


@dataclass
class UnitEconomics:
    monthly_price: float
    gross_margin: float  # 0–1, after hosting, API/inference, payment fees, support
    monthly_churn: float  # 0–1, share of paying customers lost per month
    acquisition_spend: float  # total S&M spend in the period, incl. failed spend
    founder_hours: float = 0.0  # time spent on acquisition in the period
    founder_hourly_cost: float = 0.0  # opportunity cost per hour
    customers_won: int = 1
    cost_of_capital: float = 0.20  # yearly discount rate; early-stage risk is high
    horizon_years: int = 5

    @property
    def cac(self) -> float:
        total = self.acquisition_spend + self.founder_hours * self.founder_hourly_cost
        return total / max(self.customers_won, 1)

    @property
    def monthly_gross_profit(self) -> float:
        return self.monthly_price * self.gross_margin

    @property
    def ltv(self) -> float:
        """Discounted gross profit per customer over the horizon, with churn."""
        retention = 1.0 - self.monthly_churn
        total = 0.0
        for month in range(self.horizon_years * 12):
            survival = retention**month
            discount = (1.0 + self.cost_of_capital) ** (month / 12)
            total += self.monthly_gross_profit * survival / discount
        return total

    @property
    def ltv_to_cac(self) -> float:
        return self.ltv / self.cac if self.cac else float("inf")

    @property
    def payback_months(self) -> float:
        """Months of gross profit needed to recover CAC (ignores churn and discounting)."""
        if self.monthly_gross_profit <= 0:
            return float("inf")
        return self.cac / self.monthly_gross_profit

    def report(self, currency: str = "EUR") -> str:
        lines = [
            f"CAC:               {self.cac:,.0f} {currency}",
            f"LTV ({self.horizon_years}y, disc.):   {self.ltv:,.0f} {currency}",
            f"LTV / CAC:         {self.ltv_to_cac:.1f}x  (rule of thumb: >= 3x)",
            f"CAC payback:       {self.payback_months:.1f} months  (rule of thumb: <= 12)",
            f"Avg. lifetime:     {1 / self.monthly_churn:.0f} months"
            if self.monthly_churn
            else "Avg. lifetime:     unbounded (churn = 0 — check this)",
        ]
        return "\n".join(lines)


if __name__ == "__main__":
    # Example inputs only — replace every number with a sourced or measured value.
    tam_bottom_up = bottom_up_tam(customers=25_000, annual_revenue_per_customer=60)
    tam_top_down = top_down_tam(market_size=40_000_000, share_matching_profile=0.05)
    print(f"Bottom-up TAM: {tam_bottom_up:,.0f} EUR")
    print(f"Top-down TAM:  {tam_top_down:,.0f} EUR")
    ratio = max(tam_bottom_up, tam_top_down) / min(tam_bottom_up, tam_top_down)
    if ratio > 10:
        print("Warning: estimates differ by more than 10x — revisit the assumptions.")
    print()

    example = UnitEconomics(
        monthly_price=5.0,
        gross_margin=0.80,
        monthly_churn=0.06,
        acquisition_spend=300.0,
        founder_hours=20,
        founder_hourly_cost=15.0,
        customers_won=40,
    )
    print(example.report())

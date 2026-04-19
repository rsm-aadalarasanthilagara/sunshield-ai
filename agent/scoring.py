"""
Component scoring functions for the SunShield site optimizer.
Each function returns a score in [0, 100].
"""

import os


def calculate_heat_risk_score(temp_delta: float) -> float:
    """
    Normalize temp_delta to 0-100 scale.
    - Max observed temp_delta is ~5.0
    - Formula: (temp_delta / 5.0) * 100
    - Cap at 100
    """
    return min((temp_delta / 5.0) * 100, 100.0)


def calculate_solar_potential_score(sun_hours_daily: float) -> float:
    """
    Normalize sun hours to 0-100 scale.
    - Ideal is 9 hours (100 points)
    - Formula: (sun_hours_daily / 9.0) * 100
    - Our sites all get ~6 hours = 67 points (realistic!)
    """
    return min((sun_hours_daily / 9.0) * 100, 100.0)


def calculate_public_impact_score(pedestrians_per_day: int) -> float:
    """
    Normalize pedestrian count to 0-100 scale.
    - Max observed is ~500 people
    - Formula: (pedestrians_per_day / 500) * 100
    - Cap at 100
    """
    return min((pedestrians_per_day / 500) * 100, 100.0)


def calculate_feasibility_score(installation_cost: float, has_grid_access: bool) -> float:
    """
    Feasibility: lower cost + infrastructure = higher score.
    Target ranges:
      Easy  (low cost + grid):  70-90
      Medium:                   50-70
      Hard  (high cost, no grid): 30-50

    Cost scaled so $25k → 80 pts, $40k → 40 pts.
    Grid bonus: +20 | No grid penalty: -10
    Final clamped to 30-95.
    """
    cost_score = ((45_000 - installation_cost) / 20_000) * 80
    cost_score = max(20.0, min(80.0, cost_score))
    grid_bonus = 20.0 if has_grid_access else -10.0
    return max(30.0, min(95.0, cost_score + grid_bonus))


def calculate_dual_benefit_score(site_row) -> dict:
    """
    Weighted combination of all 4 components.

    Input: pandas Series (one row from ucsd_sites_final.csv)

    Returns dict with all component scores + weighted composite:
      heat_risk:      40%
      solar_potential: 30%
      public_impact:  20%
      feasibility:    10%
    """
    heat = calculate_heat_risk_score(site_row["temp_delta"])
    solar = calculate_solar_potential_score(site_row["sun_hours_daily"])
    impact = calculate_public_impact_score(site_row["pedestrians_per_day"])
    feasibility = calculate_feasibility_score(
        site_row["installation_cost"],
        bool(site_row["has_grid_access"]),
    )

    composite = (
        0.40 * heat
        + 0.30 * solar
        + 0.20 * impact
        + 0.10 * feasibility
    )

    return {
        "heat_risk_score":      round(heat, 2),
        "solar_potential_score": round(solar, 2),
        "public_impact_score":  round(impact, 2),
        "feasibility_score":    round(feasibility, 2),
        "dual_benefit_score":   round(composite, 2),
    }


# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import pandas as pd

    # Anchor path to this file's location so it works from any directory
    _HERE = os.path.dirname(os.path.abspath(__file__))
    FINAL_CSV = os.path.join(_HERE, "../data/processed/ucsd_sites_final.csv")
    SCORED_CSV = os.path.join(_HERE, "../data/processed/ucsd_sites_scored.csv")

    df = pd.read_csv(FINAL_CSV)

    for idx, site in df.iterrows():
        scores = calculate_dual_benefit_score(site)
        df.at[idx, "heat_risk_score"]       = scores["heat_risk_score"]
        df.at[idx, "solar_potential_score"]  = scores["solar_potential_score"]
        df.at[idx, "public_impact_score"]    = scores["public_impact_score"]
        df.at[idx, "feasibility_score"]      = scores["feasibility_score"]
        df.at[idx, "dual_benefit_score"]     = scores["dual_benefit_score"]

    df_sorted = df.sort_values("dual_benefit_score", ascending=False)

    print("\n=== TOP 5 RECOMMENDED SITES ===\n")
    print(df_sorted[[
        "site_id", "name", "dual_benefit_score",
        "heat_risk_score", "solar_potential_score",
        "public_impact_score", "feasibility_score",
    ]].head(5).to_string(index=False))

    df_sorted.to_csv(SCORED_CSV, index=False)
    print(f"\nSaved scored sites to {SCORED_CSV}")

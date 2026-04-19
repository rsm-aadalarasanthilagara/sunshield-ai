"""
Site ranking and budget optimization for the SunShield agent.
Run directly to test against ucsd_sites_final.csv.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from scoring import calculate_dual_benefit_score


def rank_sites(sites_df: pd.DataFrame) -> pd.DataFrame:
    """Score every site, attach component scores, return sorted by dual_benefit_score desc."""
    df = sites_df.copy()

    score_cols = df.apply(
        lambda row: pd.Series(calculate_dual_benefit_score(row)), axis=1
    )
    df = pd.concat([df, score_cols], axis=1)

    return df.sort_values("dual_benefit_score", ascending=False).reset_index(drop=True)


def optimize_budget(sites_df: pd.DataFrame, budget: float) -> dict:
    """
    Greedy selection: pick highest-scoring sites within budget.
    Returns selected sites DataFrame + summary metrics.
    """
    ranked = rank_sites(sites_df)
    selected_rows = []
    spent = 0.0

    for _, row in ranked.iterrows():
        cost = row["installation_cost"]
        if spent + cost <= budget:
            selected_rows.append(row)
            spent += cost

    if not selected_rows:
        return {
            "selected": pd.DataFrame(),
            "sites_count": 0,
            "total_cost": 0,
            "total_kwh_per_year": 0,
            "people_impacted": 0,
            "avg_score": 0,
        }

    selected = pd.DataFrame(selected_rows).reset_index(drop=True)
    return {
        "selected": selected,
        "sites_count": len(selected),
        "total_cost": round(spent, 0),
        "total_kwh_per_year": round(selected["estimated_kwh_per_year"].sum(), 0),
        "people_impacted": int(selected["pedestrians_per_day"].sum()),
        "avg_score": round(selected["dual_benefit_score"].mean(), 2),
    }


# ── Test runner ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _HERE = os.path.dirname(os.path.abspath(__file__))
    CANDIDATES = [
        os.path.join(_HERE, "../data/processed/ucsd_sites_final.csv"),
        os.path.join(_HERE, "../data/processed/ucsd_sites_enriched.csv"),
        os.path.join(_HERE, "../data/processed/ucsd_hotspots.csv"),
    ]

    csv_path = next((p for p in CANDIDATES if os.path.exists(p)), None)
    if csv_path is None:
        print("No site CSV found. Run process_scripps_data.py first.")
        sys.exit(1)

    print(f"Loading: {os.path.basename(csv_path)}\n")
    df = pd.read_csv(csv_path)

    # ── Rank all sites ────────────────────────────────────────────────────────
    ranked = rank_sites(df)

    print("=" * 72)
    print("TOP 5 SITES BY DUAL BENEFIT SCORE")
    print("=" * 72)
    print(ranked[[
        "site_id", "name", "dual_benefit_score",
        "heat_risk_score", "solar_potential_score",
        "public_impact_score", "feasibility_score",
    ]].head(5).to_string(index=False))

    print("\n" + "=" * 72)
    print("SCORE BREAKDOWN — TOP 5")
    print("=" * 72)
    for _, row in ranked.head(5).iterrows():
        print(
            f"  {row['site_id']}  {row['name']:<35}"
            f"  TOTAL={row['dual_benefit_score']:>5.1f}"
            f"  heat={row['heat_risk_score']:>5.1f}"
            f"  solar={row['solar_potential_score']:>5.1f}"
            f"  impact={row['public_impact_score']:>5.1f}"
            f"  feasibility={row['feasibility_score']:>5.1f}"
        )

    # ── Budget optimization ───────────────────────────────────────────────────
    TEST_BUDGET = 200_000
    print(f"\n{'=' * 72}")
    print(f"BUDGET OPTIMIZATION — ${TEST_BUDGET:,.0f}")
    print("=" * 72)
    result = optimize_budget(df, budget=TEST_BUDGET)

    print(f"  Sites selected   : {result['sites_count']}")
    print(f"  Total cost       : ${result['total_cost']:>10,.0f}")
    print(f"  kWh/year         : {result['total_kwh_per_year']:>10,.0f}")
    print(f"  People impacted  : {result['people_impacted']:>10,}")
    print(f"  Avg score        : {result['avg_score']:>10.2f}")

    if not result["selected"].empty:
        print("\n  Selected sites:")
        for _, r in result["selected"].iterrows():
            print(
                f"    {r['site_id']}  {r['name']:<35}"
                f"  score={r['dual_benefit_score']:.1f}"
                f"  cost=${r['installation_cost']:,.0f}"
            )

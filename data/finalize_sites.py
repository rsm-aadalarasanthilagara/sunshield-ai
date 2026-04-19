"""
Finalize enriched site data with site type, foot traffic, cost, and grid access.
Input:  <script_dir>/processed/ucsd_sites_enriched.csv
Output: <script_dir>/processed/ucsd_sites_final.csv
Paths are anchored to this file's location so the script runs from any directory.
"""

import os
import random
import pandas as pd

random.seed(42)  # reproducible results for demo

_HERE = os.path.dirname(os.path.abspath(__file__))
IN_FILE = os.path.join(_HERE, "processed", "ucsd_sites_enriched.csv")
OUT_FILE = os.path.join(_HERE, "processed", "ucsd_sites_final.csv")


def classify_site_type(name: str) -> str:
    n = name.lower()
    if "parking" in n:
        return "parking_structure"
    if "plaza" in n or "mall" in n or "quad" in n:
        return "plaza"
    if "canyon" in n or "loop" in n or "lane" in n:
        return "walkway"
    return "remote"


def pedestrians_per_day(site_type: str) -> int:
    ranges = {
        "parking_structure": (400, 500),
        "plaza":             (250, 350),
        "walkway":           (300, 400),
        "remote":            (100, 200),
    }
    lo, hi = ranges[site_type]
    return random.randint(lo, hi)


def installation_cost(site_type: str) -> int:
    base = 30_000
    premiums = {
        "parking_structure":  8_000,
        "plaza":              2_000,
        "walkway":                0,
        "remote":            -3_000,
    }
    variation = random.randint(-2_000, 3_000)
    return base + premiums[site_type] + variation


def has_grid_access(site_type: str) -> bool:
    probabilities = {
        "parking_structure": 1.00,
        "plaza":             0.90,
        "walkway":           0.80,
        "remote":            0.60,
    }
    return random.random() < probabilities[site_type]


def finalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["site_type"] = df["name"].apply(classify_site_type)
    df["pedestrians_per_day"] = df["site_type"].apply(pedestrians_per_day)
    df["installation_cost"] = df["site_type"].apply(installation_cost)
    df["has_grid_access"] = df["site_type"].apply(has_grid_access)

    return df


def main() -> None:
    if not os.path.exists(IN_FILE):
        raise FileNotFoundError(
            f"{IN_FILE} not found. Run enrich_solar_data.py first.\n"
            f"(Run from project root: python src/data/enrich_solar_data.py)"
        )

    df = pd.read_csv(IN_FILE)
    print(f"Loaded {len(df)} sites from {IN_FILE}")

    final = finalize(df)

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    final.to_csv(OUT_FILE, index=False)
    print(f"Wrote {len(final)} rows to {OUT_FILE}\n")

    preview = final[[
        "site_id", "name", "site_type",
        "pedestrians_per_day", "installation_cost", "has_grid_access",
    ]]
    print(preview.to_string(index=False))


if __name__ == "__main__":
    main()

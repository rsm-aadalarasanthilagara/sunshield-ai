"""
Enrich ucsd_hotspots.csv with NREL PVWatts solar data.
Input:  ./processed/ucsd_hotspots.csv
Output: ./processed/ucsd_sites_enriched.csv
"""

import os
import time
import random
import requests
import pandas as pd
from dotenv import load_dotenv

random.seed(42)

load_dotenv(dotenv_path="../../.env")

NREL_API_KEY = os.environ["NREL_API_KEY"]
NREL_URL = "https://developer.nrel.gov/api/pvwatts/v8.json"

IN_FILE = "./processed/ucsd_hotspots.csv"
OUT_FILE = "./processed/ucsd_sites_enriched.csv"

# Shade canopy system assumptions (10 kW is a realistic solar canopy per site)
SYSTEM_CAPACITY_KW = 10
AZIMUTH = 180  # south-facing
TILT = 20  # optimal for San Diego latitude
ARRAY_TYPE = 1  # fixed roof/canopy mount
MODULE_TYPE = 0  # standard
LOSSES = 14  # default system losses %


def fetch_nrel(lat: float, lon: float) -> dict:
    """Call PVWatts v8 and return parsed solar metrics."""
    params = {
        "api_key": NREL_API_KEY,
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        "system_capacity": SYSTEM_CAPACITY_KW,
        "azimuth": AZIMUTH,
        "tilt": TILT,
        "array_type": ARRAY_TYPE,
        "module_type": MODULE_TYPE,
        "losses": LOSSES,
        "timeframe": "monthly",
    }
    resp = requests.get(NREL_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if "outputs" not in data:
        raise ValueError(f"Unexpected NREL response: {data.get('errors', data)}")

    outputs = data["outputs"]
    return {
        # solrad_annual = avg daily solar radiation (kWh/m²/day) ≈ peak sun hours
        "sun_hours_daily": round(outputs["solrad_annual"], 2),
        # ac_annual = estimated annual AC energy for a 10 kW canopy system (kWh/yr)
        "estimated_kwh_per_year": round(outputs["ac_annual"], 0),
    }


def _site_type_from_name(name: str) -> str:
    """Mirror the classify_site_type logic from finalize_sites.py."""
    n = name.lower()
    if "parking" in n:
        return "parking_structure"
    if "plaza" in n or "mall" in n or "quad" in n:
        return "plaza"
    if "canyon" in n or "loop" in n or "lane" in n:
        return "walkway"
    return "remote"


def _sun_modifier(site_type: str) -> float:
    """
    Apply realistic shading factor based on site type.
    parking_structure: elevated, less shade → 1.10–1.20
    plaza:             open spaces          → 1.00–1.10
    walkway:           some tree shading    → 0.95–1.05
    remote:            building shadows     → 0.90–1.00
    """
    ranges = {
        "parking_structure": (1.10, 1.20),
        "plaza":             (1.00, 1.10),
        "walkway":           (0.95, 1.05),
        "remote":            (0.90, 1.00),
    }
    lo, hi = ranges[site_type]
    return random.uniform(lo, hi)


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    sun_hours = []
    kwh_per_year = []

    for i, row in df.iterrows():
        site_id = row["site_id"]
        try:
            result = fetch_nrel(row["latitude"], row["longitude"])
            base_sun = result["sun_hours_daily"]
            site_type = _site_type_from_name(row["name"])
            modifier = _sun_modifier(site_type)
            adjusted_sun = round(base_sun * modifier, 2)
            # Scale kWh proportionally to the adjusted sun hours
            adjusted_kwh = round(result["estimated_kwh_per_year"] * modifier, 0)

            sun_hours.append(adjusted_sun)
            kwh_per_year.append(adjusted_kwh)
            print(
                f"  {site_id} [{site_type:<17}]: "
                f"base={base_sun} × {modifier:.3f} → {adjusted_sun} sun-hrs/day, "
                f"{adjusted_kwh:,.0f} kWh/yr"
            )
        except Exception as e:
            print(f"  {site_id}: NREL call failed — {e}. Using fallback.")
            sun_hours.append(5.6)
            kwh_per_year.append(16400.0)

        # Stay within NREL rate limit (1 req/sec for demo key)
        time.sleep(1.1)

    df = df.copy()
    df["sun_hours_daily"] = sun_hours
    df["estimated_kwh_per_year"] = kwh_per_year
    return df


def main() -> None:
    df = pd.read_csv(IN_FILE)
    print(f"Loaded {len(df)} sites from {IN_FILE}")
    print(f"Calling NREL PVWatts API for each site (~{len(df)} seconds)...\n")

    enriched = enrich(df)

    enriched.to_csv(OUT_FILE, index=False)
    print(f"\nWrote {len(enriched)} rows to {OUT_FILE}")
    print(
        enriched[
            ["site_id", "name", "sun_hours_daily", "estimated_kwh_per_year"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()

"""
Process ZenPower solar permit data into benchmark metrics.
Converted from starter_notebook.ipynb (polars+Supabase) to plain pandas+CSV.

Input:  ../../data/raw/zenpower-challenge/records.csv
        ../../data/raw/zenpower-challenge/solar-city-permits.csv
Output: ../../data/processed/solar_benchmarks.csv
        ../../data/processed/solar_city_enriched.csv
"""

import os
import pandas as pd

RAW_DIR = "../../data/raw/zenpower-challenge"
OUT_DIR = "../../data/processed"

RECORDS_FILE = os.path.join(RAW_DIR, "records.csv")
SOLAR_CITY_FILE = os.path.join(RAW_DIR, "solar-city-permits.csv")

# These columns mirror the Supabase records table from the notebook
RECORDS_COLUMNS = [
    "id", "created_at", "source_id", "source_type", "permit_id", "permit_type",
    "kind", "company_name", "kilowatt_value", "issue_date", "apply_date",
    "latitude", "longitude", "full_address", "city", "state", "county",
    "postal_code", "is_active", "is_system_size_estimation",
]


def load_records() -> pd.DataFrame:
    print("Loading records.csv...")
    df = pd.read_csv(RECORDS_FILE, usecols=RECORDS_COLUMNS, low_memory=False)
    print(f"  {len(df)} rows, {df['city'].nunique()} unique cities")

    # Parse dates
    df["issue_date"] = pd.to_datetime(df["issue_date"], utc=True, errors="coerce")
    df["apply_date"] = pd.to_datetime(df["apply_date"], utc=True, errors="coerce")

    # Only rows with a valid kW reading
    df = df[df["kilowatt_value"].notna() & (df["kilowatt_value"] > 0)].copy()
    print(f"  {len(df)} rows with valid kilowatt_value")
    return df


def load_solar_city() -> pd.DataFrame:
    print("Loading solar-city-permits.csv...")
    # Only pull columns we actually use
    use_cols = [
        "BIZ_NAME", "ISSUE_DATE", "JOB_VALUE", "FEES",
        "APPROVAL_DURATION", "INSPECTION_PASS_RATE", "INSPECTION_PASSED",
        "DESCRIPTION", "CITY", "STATE", "LAT", "LONG",
        "BATTERY", "SOLAR", "PROPERTY_TYPE",
        "PROPERTY_ASSESS_MARKET_VALUE", "PROPERTY_BUILDING_AREA",
    ]
    df = pd.read_csv(SOLAR_CITY_FILE, usecols=use_cols, low_memory=False)
    df.columns = [c.lower() for c in df.columns]
    df["issue_date"] = pd.to_datetime(df["issue_date"], errors="coerce")
    df = df[df["job_value"].notna() & (df["job_value"] > 0)].copy()
    print(f"  {len(df)} rows with valid job_value")
    return df


def build_city_benchmarks(records: pd.DataFrame) -> pd.DataFrame:
    """Per-city solar install summary from the main records table."""
    records["issue_year_month"] = records["issue_date"].dt.to_period("M")

    # Monthly install counts per city (for install velocity)
    monthly = (
        records.groupby(["city", "state", "issue_year_month"])
        .size()
        .reset_index(name="monthly_installs")
    )
    velocity = (
        monthly.groupby(["city", "state"])["monthly_installs"]
        .mean()
        .reset_index(name="avg_installs_per_month")
    )

    # Core aggregations
    agg = (
        records.groupby(["city", "state"])
        .agg(
            total_installs=("id", "count"),
            avg_kw=("kilowatt_value", "mean"),
            median_kw=("kilowatt_value", "median"),
            total_kw=("kilowatt_value", "sum"),
        )
        .reset_index()
    )

    benchmarks = agg.merge(velocity, on=["city", "state"], how="left")
    benchmarks = benchmarks.sort_values("total_installs", ascending=False)
    return benchmarks


def build_cost_benchmarks(solar_city: pd.DataFrame) -> pd.DataFrame:
    """Cost-per-kW estimates from SolarCity permit job values."""
    # Extract kW from description text (e.g. "install 2.95 kw ...")
    solar_city["kw_from_desc"] = (
        solar_city["description"]
        .str.extract(r"(\d+\.?\d*)\s*kw", flags=2)  # case-insensitive
        .astype(float)
    )

    has_kw = solar_city[solar_city["kw_from_desc"].notna() & (solar_city["kw_from_desc"] > 0)].copy()
    has_kw["cost_per_kw"] = has_kw["job_value"] / has_kw["kw_from_desc"]

    # Sanity filter: $500–$8000/kW is a realistic range
    has_kw = has_kw[(has_kw["cost_per_kw"] >= 500) & (has_kw["cost_per_kw"] <= 8000)]

    cost_agg = (
        has_kw.groupby(["city", "state"])
        .agg(
            avg_job_value=("job_value", "mean"),
            avg_cost_per_kw=("cost_per_kw", "mean"),
            median_cost_per_kw=("cost_per_kw", "median"),
            avg_approval_days=("approval_duration", "mean"),
            avg_inspection_pass_rate=("inspection_pass_rate", "mean"),
            n_permits=("job_value", "count"),
        )
        .reset_index()
    )
    return cost_agg


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    records = load_records()
    solar_city = load_solar_city()

    # City-level install benchmarks from records
    benchmarks = build_city_benchmarks(records)
    out_path = os.path.join(OUT_DIR, "solar_benchmarks.csv")
    benchmarks.to_csv(out_path, index=False)
    print(f"\nWrote {len(benchmarks)} city rows to {out_path}")
    print(benchmarks.head(10).to_string(index=False))

    # Cost benchmarks from SolarCity permits
    costs = build_cost_benchmarks(solar_city)
    cost_path = os.path.join(OUT_DIR, "solar_city_costs.csv")
    costs.to_csv(cost_path, index=False)
    print(f"\nWrote {len(costs)} cost rows to {cost_path}")
    print(costs.head(10).to_string(index=False))


if __name__ == "__main__":
    main()

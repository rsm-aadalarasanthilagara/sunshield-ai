"""
Process all Scripps bike/walk heat data files into candidate shading sites.
Input:  ./raw/*.txt  (space-separated: Time LAT LONG ALT Temp RH)
Output: ./processed/ucsd_hotspots.csv
"""

import os
import glob
import pandas as pd
from sklearn.cluster import DBSCAN

LANDMARKS = [
    (32.8768, -117.2359, "Gilman Transit Area"),
    (32.8794, -117.2359, "Warren Mall"),
    (32.8751, -117.2375, "Geisel Plaza"),
    (32.8810, -117.2340, "Warren College"),
    (32.8733, -117.2411, "Price Center"),
    (32.8762, -117.2411, "Revelle Plaza"),
    (32.8780, -117.2395, "Muir Quad"),
    (32.8800, -117.2380, "Marshall College"),
    (32.8745, -117.2350, "Pepper Canyon"),
    (32.8720, -117.2370, "Rady School Area"),
    (32.8755, -117.2330, "Pangea Parking"),
    (32.8790, -117.2330, "Hopkins Parking Structure"),
    (32.8730, -117.2390, "Central Campus Loop"),
    (32.8810, -117.2390, "Muir College Drive"),
    (32.8770, -117.2340, "Gilman Dr East"),
    (32.8760, -117.2360, "Health Sciences Loop"),
    (32.8740, -117.2360, "Library Walk"),
    (32.8800, -117.2360, "Eleanor Roosevelt College"),
    (32.8820, -117.2370, "Sixth College"),
    (32.8715, -117.2380, "Osler Lane"),
    (32.8825, -117.2355, "North Campus"),
    (32.8710, -117.2360, "South Campus"),
    (32.8760, -117.2380, "Sun God Lawn"),
    (32.8780, -117.2370, "Mandeville Terrace"),
    (32.8750, -117.2400, "Cross-Cultural Center"),
]

RAW_DIR = "./raw"
OUT_FILE = "./processed/ucsd_hotspots.csv"

LAT_MIN, LAT_MAX = 32.87, 32.88
LON_MIN, LON_MAX = -117.24, -117.23

# ~11m radius per cluster — small enough to surface distinct hotspots
DBSCAN_EPS = 0.0001
DBSCAN_MIN_SAMPLES = 3


def nearest_landmark(lat: float, lon: float) -> str:
    dists = [((lat - lm[0]) ** 2 + (lon - lm[1]) ** 2, lm[2]) for lm in LANDMARKS]
    return min(dists, key=lambda x: x[0])[1]


def make_unique_names(raw_names: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    for name in raw_names:
        counts[name] = counts.get(name, 0) + 1

    seen: dict[str, int] = {}
    result = []
    for name in raw_names:
        if counts[name] > 1:
            seen[name] = seen.get(name, 0) + 1
            result.append(f"{name} {seen[name]}")
        else:
            result.append(name)
    return result


def load_all_files(raw_dir: str) -> pd.DataFrame:
    """Load and concatenate all .txt files in raw_dir."""
    files = glob.glob(os.path.join(raw_dir, "*.txt"))
    if not files:
        raise FileNotFoundError(f"No .txt files found in {raw_dir}")

    frames = []
    for path in sorted(files):
        try:
            df = pd.read_csv(
                path,
                sep=r"\s+",
                header=None,
                names=["Time", "LAT", "LONG", "ALT", "Temp", "RH"],
            )
            # tag each row with its source file (date prefix)
            df["source_file"] = os.path.basename(path)
            frames.append(df)
            print(f"  Loaded {len(df):>5} rows  ← {os.path.basename(path)}")
        except Exception as e:
            print(f"  SKIP {os.path.basename(path)}: {e}")

    combined = pd.concat(frames, ignore_index=True)
    print(f"\nTotal rows across all files: {len(combined)}")
    return combined


def process() -> pd.DataFrame:
    # 1. Load all files
    print("Loading files from", RAW_DIR)
    df = load_all_files(RAW_DIR)

    # 2. Filter to UCSD campus bounding box
    df = df[
        df["LAT"].between(LAT_MIN, LAT_MAX) &
        df["LONG"].between(LON_MIN, LON_MAX)
    ].copy()
    print(f"On-campus rows after bbox filter: {len(df)}")

    if df.empty:
        raise ValueError("No rows within UCSD campus bounds — check data files.")

    # 3. Campus baseline temp
    campus_avg_temp = df["Temp"].mean()
    campus_std_temp = df["Temp"].std()
    print(f"Campus avg temp: {campus_avg_temp:.2f} C  std: {campus_std_temp:.2f} C")

    # 4. DBSCAN — small eps to surface distinct ~11m hotspot zones
    coords = df[["LAT", "LONG"]].values
    db = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN_SAMPLES).fit(coords)
    df["cluster"] = db.labels_

    n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    noise = (db.labels_ == -1).sum()
    print(f"DBSCAN found {n_clusters} clusters ({noise} noise points dropped)")

    # 5. Aggregate per cluster
    clustered = df[df["cluster"] != -1]
    agg = (
        clustered.groupby("cluster")
        .agg(
            latitude=("LAT", "mean"),
            longitude=("LONG", "mean"),
            avg_temp=("Temp", "mean"),
            point_count=("Temp", "count"),
        )
        .reset_index(drop=True)
    )
    agg["temp_delta"] = agg["avg_temp"] - campus_avg_temp

    # 6. Name each cluster by nearest landmark
    raw_names = [
        nearest_landmark(float(row["latitude"]), float(row["longitude"]))
        for _, row in agg.iterrows()
    ]
    agg["name"] = make_unique_names(raw_names)

    # 7. Top 25 hottest sites
    agg = agg.sort_values("temp_delta", ascending=False).head(25).reset_index(drop=True)
    agg.insert(0, "site_id", [f"SITE_{i + 1:02d}" for i in range(len(agg))])

    return agg[["site_id", "name", "latitude", "longitude", "avg_temp", "temp_delta", "point_count"]]


def main() -> None:
    os.makedirs("./processed", exist_ok=True)

    sites = process()

    sites.to_csv(OUT_FILE, index=False)
    print(f"\nWrote {len(sites)} sites to {OUT_FILE}")
    print(sites.to_string(index=False))


if __name__ == "__main__":
    main()

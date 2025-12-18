"""Build region-year aggregates from the UNCTAD digital services trade panel."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = PROJECT_ROOT / "datasets"
PANEL_FILE = DATASETS_DIR / "unctad_country_year_digital_services_trade_panel.csv"

OUTPUT_FILE = DATASETS_DIR / "unctad_regional_aggregates_dig_services_trade_by_year.csv"

EXPORTS_COLUMN = "dig_services_exports_usd_millions"
IMPORTS_COLUMN = "dig_services_imports_usd_millions"

ASEAN_ISO3: set[str] = {
    "BRN",
    "KHM",
    "IDN",
    "LAO",
    "MYS",
    "MMR",
    "PHL",
    "SGP",
    "THA",
    "VNM",
}

EU27_ISO3: set[str] = {
    "AUT",
    "BEL",
    "BGR",
    "HRV",
    "CYP",
    "CZE",
    "DNK",
    "EST",
    "FIN",
    "FRA",
    "DEU",
    "GRC",
    "HUN",
    "IRL",
    "ITA",
    "LVA",
    "LTU",
    "LUX",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "ESP",
    "SWE",
}

G7_ISO3: set[str] = {"CAN", "FRA", "DEU", "ITA", "JPN", "GBR", "USA"}

REGION_MEMBERS: dict[str, set[str]] = {
    "ASEAN": ASEAN_ISO3,
    "EU27": EU27_ISO3,
    "G7": G7_ISO3,
}

AGGREGATE_ISO3_CODES: set[str] = {"WLD", "SSF"}
AGGREGATE_COUNTRY_LABELS: set[str] = {"World", "Sub-Saharan Africa"}


def load_panel(path: Path) -> pd.DataFrame:
    """Load the pre-built country-year panel dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Panel file not found at {path}. Run scripts/build_unctad_de_panel.py first."
        )
    return pd.read_csv(path)


def filter_countries_only(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out aggregate geographies such as World (WLD)."""
    required_columns = {"iso3", "country"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {sorted(missing_columns)}")

    filtered = df.copy()
    filtered = filtered[~filtered["iso3"].isin(AGGREGATE_ISO3_CODES)]
    filtered = filtered[~filtered["country"].isin(AGGREGATE_COUNTRY_LABELS)]
    return filtered


def build_region_year_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate exports/imports totals by region and year."""
    required_columns = {"iso3", "year", EXPORTS_COLUMN, IMPORTS_COLUMN}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {sorted(missing_columns)}")

    base = df.copy()
    base["year"] = pd.to_numeric(base["year"], errors="coerce").astype("Int64")
    base[EXPORTS_COLUMN] = pd.to_numeric(base[EXPORTS_COLUMN], errors="coerce")
    base[IMPORTS_COLUMN] = pd.to_numeric(base[IMPORTS_COLUMN], errors="coerce")

    rows: list[pd.DataFrame] = []
    for region, members in REGION_MEMBERS.items():
        region_df = base[base["iso3"].isin(members)].copy()
        grouped = (
            region_df.groupby("year", dropna=True)
            .agg(
                dig_services_exports_usd_millions_total=(EXPORTS_COLUMN, "sum"),
                dig_services_imports_usd_millions_total=(IMPORTS_COLUMN, "sum"),
                num_reporting_exports=(EXPORTS_COLUMN, "count"),
                num_reporting_imports=(IMPORTS_COLUMN, "count"),
            )
            .reset_index()
        )
        grouped["region"] = region
        grouped["num_members"] = len(members)
        rows.append(grouped)

    result = pd.concat(rows, ignore_index=True)
    result = result[
        [
            "region",
            "year",
            "num_members",
            "num_reporting_exports",
            "num_reporting_imports",
            "dig_services_exports_usd_millions_total",
            "dig_services_imports_usd_millions_total",
        ]
    ].sort_values(["region", "year"], ascending=True)
    return result.reset_index(drop=True)


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-aggregates",
        action="store_true",
        help="Keep aggregate geographies in the input panel (not recommended).",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    panel = load_panel(PANEL_FILE)
    if not args.include_aggregates:
        panel = filter_countries_only(panel)

    aggregates = build_region_year_aggregates(panel)
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    aggregates.to_csv(OUTPUT_FILE, index=False)
    logging.info("Wrote %s rows to %s", len(aggregates), OUTPUT_FILE)


if __name__ == "__main__":
    main()

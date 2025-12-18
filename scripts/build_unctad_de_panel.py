"""Build a country-year panel dataset from UNCTAD Digital Economy (Data360) exports."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = PROJECT_ROOT / "datasets"
INPUT_FILE = DATASETS_DIR / "UNCTAD_DE.csv"
OUTPUT_FILE = DATASETS_DIR / "unctad_country_year_digital_services_trade_panel.csv"

EXPORTS_INDICATOR = "UNCTAD_DE_DIG_SERVTRADE_ANN_EXP"
IMPORTS_INDICATOR = "UNCTAD_DE_DIG_SERVTRADE_ANN_IMP"

INDICATOR_COLUMN_MAP: dict[str, str] = {
    EXPORTS_INDICATOR: "dig_services_exports_usd_millions",
    IMPORTS_INDICATOR: "dig_services_imports_usd_millions",
}

STATUS_PRIORITY: dict[str, int] = {
    "A": 0,
    "E": 1,
    "P": 2,
    "O": 3,
}


def load_unctad_de(path: Path) -> pd.DataFrame:
    """Load the UNCTAD_DE Data360 extract."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path)


def _normalize_to_millions(obs_value: pd.Series, unit_mult: pd.Series) -> pd.Series:
    """Normalize values to a 'millions' unit multiplier."""
    unit_mult_numeric = pd.to_numeric(unit_mult, errors="coerce")
    exponent = unit_mult_numeric - 6
    multiplier = np.power(10.0, exponent)
    return obs_value * multiplier


def build_country_year_panel(df: pd.DataFrame) -> pd.DataFrame:
    """Create a country-year panel for digital services trade exports/imports."""
    required_columns = {
        "REF_AREA",
        "REF_AREA_LABEL",
        "INDICATOR",
        "TIME_PERIOD",
        "OBS_VALUE",
        "UNIT_MULT",
        "FREQ",
        "SEX",
        "AGE",
        "URBANISATION",
        "COMP_BREAKDOWN_1",
        "COMP_BREAKDOWN_2",
        "COMP_BREAKDOWN_3",
        "OBS_STATUS",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {sorted(missing_columns)}")

    filtered = df[df["INDICATOR"].isin(list(INDICATOR_COLUMN_MAP.keys()))].copy()
    filtered = filtered[filtered["FREQ"] == "A"]

    breakdown_filters: dict[str, str] = {
        "SEX": "_T",
        "AGE": "_T",
        "URBANISATION": "_T",
        "COMP_BREAKDOWN_1": "_Z",
        "COMP_BREAKDOWN_2": "_Z",
        "COMP_BREAKDOWN_3": "_Z",
    }
    for column, expected in breakdown_filters.items():
        filtered = filtered[filtered[column] == expected]

    filtered["year"] = pd.to_numeric(filtered["TIME_PERIOD"], errors="coerce").astype(
        "Int64"
    )
    filtered["obs_value"] = pd.to_numeric(filtered["OBS_VALUE"], errors="coerce")
    filtered["obs_value_millions"] = _normalize_to_millions(
        filtered["obs_value"], filtered["UNIT_MULT"]
    )

    filtered["status_priority"] = (
        filtered["OBS_STATUS"].astype(str).map(STATUS_PRIORITY).fillna(99).astype(int)
    )
    filtered = filtered.sort_values(
        ["REF_AREA", "year", "INDICATOR", "status_priority"], ascending=True
    )
    filtered = filtered.drop_duplicates(
        subset=["REF_AREA", "year", "INDICATOR"], keep="first"
    )

    panel = filtered.pivot(
        index=["REF_AREA", "REF_AREA_LABEL", "year"],
        columns="INDICATOR",
        values="obs_value_millions",
    )
    panel = panel.rename(columns=INDICATOR_COLUMN_MAP).reset_index()
    panel = panel.rename(columns={"REF_AREA": "iso3", "REF_AREA_LABEL": "country"})

    for column in INDICATOR_COLUMN_MAP.values():
        if column not in panel.columns:
            panel[column] = pd.NA

    panel = panel[
        [
            "country",
            "iso3",
            "year",
            "dig_services_exports_usd_millions",
            "dig_services_imports_usd_millions",
        ]
    ].sort_values(["iso3", "year"], ascending=True)

    return panel.reset_index(drop=True)


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    logging.info("Loading UNCTAD_DE data from %s", INPUT_FILE)
    df = load_unctad_de(INPUT_FILE)

    logging.info("Building country-year panel")
    panel = build_country_year_panel(df)

    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUTPUT_FILE, index=False)
    logging.info("Wrote %s rows to %s", len(panel), OUTPUT_FILE)


if __name__ == "__main__":
    main()

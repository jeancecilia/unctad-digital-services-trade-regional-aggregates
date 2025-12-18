# Regional Digital Services Trade Aggregates by Year (ASEAN, EU27, G7)

## Overview
This dataset provides region-level annual totals derived from UNCTAD Digital Economy and Technology data (via World Bank Data360 export).

It aggregates country-year values into reusable regional groupings:
- ASEAN
- EU27
- G7

## Files
- `datasets/unctad_regional_aggregates_dig_services_trade_by_year.csv`
  - Region-year totals (this dataset).
- `scripts/build_unctad_de_regional_aggregates.py`
  - Reproducible build script.

## What is measured
- Digitally-deliverable services **exports** (USD millions)
- Digitally-deliverable services **imports** (USD millions)

## Units
All value columns are in **USD millions**.

## Regions
Region membership is defined using ISO3 country codes in the build script:
- `ASEAN` (10 members)
- `EU27` (27 members)
- `G7` (7 members)

## Output columns
- `region`
  - Region name (`ASEAN`, `EU27`, `G7`).
- `year`
  - Calendar year.
- `num_members`
  - Total number of member countries in the region definition.
- `num_reporting_exports`
  - Count of member countries with non-missing exports for that year.
- `num_reporting_imports`
  - Count of member countries with non-missing imports for that year.
- `dig_services_exports_usd_millions_total`
  - Sum of members' digitally-deliverable services exports (USD millions).
- `dig_services_imports_usd_millions_total`
  - Sum of members' digitally-deliverable services imports (USD millions).

## How to reproduce
From the repository root:

```bash
python scripts/build_unctad_de_panel.py
python scripts/build_unctad_de_regional_aggregates.py
```

## Notes and limitations
- This dataset aggregates **digital services trade** only. GDP/FDI/total trade require additional source indicators not present in `UNCTAD_DE.csv`.
- Missing country values are excluded from sums; reporting counts are included to show coverage.

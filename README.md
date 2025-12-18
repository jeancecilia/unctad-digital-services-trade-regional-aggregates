# UNCTAD Digital Services Trade Regional Aggregates

Region-year aggregates (ASEAN, EU27, G7) derived from UNCTAD digitally-deliverable services trade.

## Dataset
- datasets/unctad_regional_aggregates_dig_services_trade_by_year.csv

## Backlinks
- WordPress post: https://devstackph.com/regional-digital-services-trade-aggregates-asean-eu27-g7-unctad-derived/

## How to cite
If you use this dataset, please cite it as:

> Cecilia Menzel, Jean Maurice. (2025). Regional Digital Services Trade Aggregates (ASEAN, EU27, G7) — UNCTAD Derived. GitHub repository: https://github.com/jeancecilia/unctad-digital-services-trade-regional-aggregates (accessed YYYY-MM-DD).

## Reproduce
```bash
python scripts/build_unctad_de_panel.py
python scripts/build_unctad_de_regional_aggregates.py
```

See docs/KAGGLE_DESCRIPTION.md for the full dataset description.

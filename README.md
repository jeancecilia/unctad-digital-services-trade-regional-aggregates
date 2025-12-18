# Regional Digital Services Trade Aggregates (ASEAN, EU27, G7) (2010–2023 / 2025 Edition)

## Citation & DOI
For documentation, methodology, and derived analyses, see:
https://devstackph.com/regional-digital-services-trade-aggregates-asean-eu27-g7-unctad-derived/

This dataset is archived on Zenodo with a permanent DOI:
https://doi.org/10.5281/zenodo.17971356

## Overview
This dataset provides a cleaned and structured panel of **region–year totals for digitally-deliverable services trade (exports and imports, USD millions)** for **ASEAN**, **EU27**, and **G7**, derived from official source data published by **UN Trade and Development (UNCTAD)**.

The dataset was created to support research, policy analysis, journalism, and data-driven content that requires **consistent country naming, comparable time series, and ready-to-use rankings**.

**Canonical dataset page:**  
https://devstackph.com/regional-digital-services-trade-aggregates-asean-eu27-g7-unctad-derived/

---

## Source Data
Primary source:
- **UN Trade and Development (UNCTAD)** – *International trade in digitally deliverable services (UNCTADstat)*  
  Original publication:
  - https://unctadstat.unctad.org/datacentre/reportInfo/US.DigitallyDeliverableServices
  - https://unctadstat.unctad.org/datacentre/dataviewer/US.DigitallyDeliverableServices

The original source data was accessed on **2025-12-18**.

---

## Data Processing & Methodology
The following transformations were applied:

1. Built a clean country-year panel in **USD millions** from the UNCTAD export.
2. Defined region membership using ISO3 country codes for ASEAN, EU27, and G7.
3. Summed member-country exports and imports by year to produce region totals.
4. Reported `num_reporting_exports` and `num_reporting_imports` to make missingness explicit.
5. Validated totals against recomputed sums from the underlying country-year panel.

No imputation was performed.

---

## Dataset Contents
Files included:

- `datasets/unctad_regional_aggregates_dig_services_trade_by_year.csv` – Main cleaned dataset
- `docs/COLUMN_DICTIONARY.md` – Column descriptions and units
- `docs/KAGGLE_DESCRIPTION.md` – Detailed derivation notes

Key fields include:
- `region`
- `year`
- `num_members`
- `num_reporting_exports`
- `num_reporting_imports`
- `dig_services_exports_usd_millions_total`
- `dig_services_imports_usd_millions_total`

---

## Intended Use
This dataset is suitable for:
- Academic research and citation
- Policy and trade analysis
- Journalism and reporting
- SEO and content marketing with verifiable data
- Comparative country and regional studies

---

## How to Cite
If you use this dataset, please cite:

> DevStackPH (2025). *Regional Digital Services Trade Aggregates (ASEAN, EU27, G7) (2010–2023 / 2025 Edition).* GitHub repository: https://github.com/jeancecilia/unctad-digital-services-trade-regional-aggregates (accessed YYYY-MM-DD).

DOI: https://doi.org/10.5281/zenodo.17971356

---

## License
This dataset is published under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

You are free to share and adapt the data, provided proper attribution is given.

---

## Related Resources
- Canonical dataset page: https://devstackph.com/regional-digital-services-trade-aggregates-asean-eu27-g7-unctad-derived/
- Base panel dataset: https://devstackph.com/unctad-digital-services-trade-panel/
- Derived rankings: https://devstackph.com/top-20-countries-by-digital-services-exports-imports-unctad-yearly-rankings/

---

## Reproduce
```bash
python scripts/build_unctad_de_panel.py
python scripts/build_unctad_de_regional_aggregates.py
```

---

## Disclaimer
This dataset is a derived work. The authors are not responsible for interpretations or conclusions drawn from the data.

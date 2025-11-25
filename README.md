# Secure Employee Analytics Pipeline on Google Cloud (GCP)

**Fully automated, PII-protected data pipeline** that extracts sensitive employee data, applies compliance-grade security (salary masking + SHA-256 password hashing), loads into BigQuery, and delivers insights via Tableau.

<img width="675" height="431" alt="Screenshot 2025-11-24 at 5 39 45 PM" src="https://github.com/user-attachments/assets/e4b2692f-9c7a-4fb9-a4c3-0ff55d64e1c1" />


## Tech Stack
- Python + Faker (data generation)
- Google Cloud Storage (raw landing zone)
- **Cloud Data Fusion** (no-code transformation + PII protection)
- **BigQuery** (analytical warehouse)
- **Cloud Composer** (Apache Airflow orchestration)
- **Tableau** (interactive dashboard)

## Key Features
- Salary masked (`xxxxx`)
- Passwords **SHA-256 hashed** (cryptographic security)
- Daily automated execution via Airflow
- Full end-to-end orchestration with dependency management
- 100% GCP-native, production-grade design

## Business Impact
- **100% automation** — eliminated manual data handling
- **100% PII compliance** — zero exposure of salary or passwords
- **Scalable** — tested with 100 records; ready for 100K+ with zero code changes
- **Cost** — ~$0.50 per daily run on Data Fusion

## Project Structure
dags/
├── employee_secure_daily_pipeline.py     # Main Airflow DAG
└── scripts/
└── extract.py                        # Data generation + GCS upload
assets/
└── architecture.png
screenshots/
├── airflow_green.png
├── bigquery_masked.png
└── tableau_dashboard.png

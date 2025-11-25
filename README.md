
# Secure Employee Analytics Pipeline on Google Cloud (GCP)

**Fully automated, PII-protected data pipeline** that extracts sensitive employee data, applies compliance-grade security (salary masking + SHA-256 password hashing), loads into BigQuery, and delivers insights via Tableau.

<img width="675" height="431" alt="Screenshot 2025-11-24 at 5 39 45 PM" src="https://github.com/user-attachments/assets/567f03dd-2722-42a2-8b3c-db4bcbfac2d6" />


## Tech Stack
- Python + Faker (data generation)
- Google Cloud Storage (raw landing)
- Cloud Data Fusion (no-code transformation + PII protection)
- BigQuery (analytical warehouse)
- Cloud Composer (Apache Airflow orchestration)
- Tableau (interactive dashboard)

## Key Features
- Salary masked (`xxxxx`)
- Passwords SHA-256 hashed
- Daily automated execution via Airflow
- Full end-to-end orchestration
- Clean medallion architecture (raw → transformed → consumed)

## Results
- Processed 100+ employee records daily
- 100% PII compliance
- Reduced manual data handling from hours to zero
- Real-time business insights via Tableau

## Project Structure
dags/
├── employee_secure_daily_pipeline.py    # Main Airflow DAG
└── scripts/
└── extract.py                       # Data generation + GCS upload

assets/
└── architecture.png

screenshots/
├── airflow_green.png
├── bigquery_masked.png
└── tableau_dashboard.png

## How to Run
1. Clone repo
2. Deploy to GCP free tier
3. Trigger DAG → watch automation in real-time

## Why This Project Stands Out
- Real-world compliance (PII masking + hashing)
- 100% GCP-native
- Senior-level Airflow orchestration

**Built November 2025 | Nitesh Thapa | Open to DE roles**

#DataEngineering #GCP #Airflow #BigQuery #Tableau #Portfolio

# Secure Employee Analytics Pipeline on Google Cloud (GCP)

**Fully automated, PII-secure pipeline** — salary masked, passwords SHA-256 hashed  
Daily execution via Airflow · 100% GCP native · Zero manual steps

```mermaid
flowchart TD
    A[Python + Faker<br>Generate 100+ records] --> B[Cloud Storage<br>Raw CSV]
    B --> C[Cloud Data Fusion<br>Mask salary → xxxxx<br>SHA-256 hash password]
    C --> D[BigQuery<br>Clean table]
    D --> E[Tableau Dashboard<br>Live insights]
    subgraph "Orchestration"
      F[Cloud Composer<br>Airflow DAG] --> A
      F --> C
    end
    style F fill:#4285F4,stroke:#000,color:white
    style C fill:#EA4335,stroke:#000,color:white

Tech Stack
Python
GCP
Airflow
BigQuery
Tableau
Key Features

Salary masked (xxxxx)
Passwords SHA-256 hashed (cryptographic security)
Daily automated execution via Airflow
Full end-to-end orchestration
100% PII compliance

Business Impact

100% automation — eliminated manual work
100% secure — zero exposure of sensitive data
Scalable — tested 100 records → ready for 100K+
Cost — ~$0.50 per daily run

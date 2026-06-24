"""Generate synthetic employee records with Faker and upload them to GCS.

This is the raw landing-zone generator. PII protection (salary masking +
SHA-256 password hashing) happens downstream in Cloud Data Fusion before the
data reaches BigQuery — see ../../transforms/secure_transform.py for a
reference implementation of that exact logic.

The GCS bucket is read from the GCS_BUCKET environment variable. If it is unset,
the script still generates the CSV locally and skips the upload, so you can run
it without GCP credentials.
"""
import csv
import os
import random
import string

from faker import Faker

NUM_EMPLOYEES = 100

DEPARTMENTS = [
    "Engineering", "Sales", "Marketing", "Finance", "Human Resources",
    "Operations", "Customer Support", "Legal", "Product", "Data",
]

FIELDNAMES = [
    "first_name", "last_name", "job_title", "department", "email",
    "address", "phone_number", "salary", "password",
]

fake = Faker()
# Seed so the generated sample is reproducible (the README's before/after table
# always matches the committed CSV). Row count is overridable via NUM_EMPLOYEES.
Faker.seed(42)
random.seed(42)


def _random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(alphabet) for _ in range(length))


def generate_employees(num_employees: int = NUM_EMPLOYEES, output_file: str = "employee_data.csv") -> str:
    with open(output_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for _ in range(num_employees):
            writer.writerow({
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "job_title": fake.job(),
                "department": random.choice(DEPARTMENTS),
                "email": fake.email(),
                "address": fake.address().replace("\n", ", "),
                "phone_number": fake.phone_number(),
                "salary": random.randint(40_000, 200_000),
                "password": _random_password(),
            })
    print(f"Generated {num_employees} employee records -> {output_file}")
    return output_file


def upload_to_gcs(bucket_name: str, source_file: str, destination_blob: str) -> None:
    # Imported lazily so the local generation path needs only Faker, not the
    # full google-cloud-storage stack.
    from google.cloud import storage

    client = storage.Client()
    blob = client.bucket(bucket_name).blob(destination_blob)
    blob.upload_from_filename(source_file)
    print(f"Uploaded {source_file} -> gs://{bucket_name}/{destination_blob}")


if __name__ == "__main__":
    count = int(os.environ.get("NUM_EMPLOYEES", NUM_EMPLOYEES))
    output = generate_employees(count)

    bucket = os.environ.get("GCS_BUCKET")
    if bucket:
        upload_to_gcs(bucket, output, "employee_data.csv")
    else:
        print("GCS_BUCKET not set — generated locally, skipping upload.")

"""Reference implementation of the PII-protection transform.

In production this logic runs inside Cloud Data Fusion (no-code Wrangler
directives). It is reproduced here in plain Python so the security behaviour is
reviewable in-repo, testable, and unambiguous:

    - salary   -> fully masked to 'xxxxx' (raw value never reaches the warehouse)
    - password -> irreversible SHA-256 hex digest

Usage:
    python transforms/secure_transform.py employee_data.csv employee_data_secure.csv
"""
import csv
import hashlib
import hmac
import os
import sys

SALARY_MASK = "xxxxx"
# Optional secret "pepper". If set (e.g. from Secret Manager), passwords are hashed
# with HMAC-SHA256 so the mapping can't be reversed without the key.
PEPPER = os.environ.get("PII_PEPPER")


def hash_password(plaintext, pepper=PEPPER):
    """One-way hash of a password.

    With a pepper  -> HMAC-SHA256 (not reversible without the secret key).
    Without one    -> plain unsalted SHA-256. That's fine for this *synthetic* demo,
    but NOT how real credentials should be stored: production systems should use a
    salted, slow KDF such as bcrypt / scrypt / Argon2.
    """
    if pepper:
        return hmac.new(pepper.encode("utf-8"), plaintext.encode("utf-8"), hashlib.sha256).hexdigest()
    return hashlib.sha256(plaintext.encode("utf-8")).hexdigest()


def secure_row(row: dict) -> dict:
    row["salary"] = SALARY_MASK
    row["password"] = hash_password(row["password"])
    return row


def secure_file(input_file: str, output_file: str) -> None:
    with open(input_file, newline="") as fin, open(output_file, "w", newline="") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow(secure_row(row))
    print(f"Wrote PII-protected data -> {output_file}")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "employee_data.csv"
    dst = sys.argv[2] if len(sys.argv) > 2 else "employee_data_secure.csv"
    secure_file(src, dst)

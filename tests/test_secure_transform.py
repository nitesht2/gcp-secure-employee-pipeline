"""Unit tests for the PII-protection transform.

Run with pytest, or standalone:  python tests/test_secure_transform.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "transforms"))
from secure_transform import hash_password, secure_row, SALARY_MASK


def test_hash_is_deterministic_and_64_hex():
    h = hash_password("hunter2")
    assert h == hash_password("hunter2")                 # same input -> same digest
    assert len(h) == 64 and all(c in "0123456789abcdef" for c in h)


def test_pepper_changes_digest():
    assert hash_password("hunter2", pepper="s3cret") != hash_password("hunter2")


def test_secure_row_masks_salary_and_hashes_password():
    out = secure_row({"salary": "123456", "password": "hunter2"})
    assert out["salary"] == SALARY_MASK
    assert out["password"] != "hunter2" and len(out["password"]) == 64


if __name__ == "__main__":
    for _name, _fn in list(globals().items()):
        if _name.startswith("test_") and callable(_fn):
            _fn()
            print(f"PASS {_name}")
    print("All tests passed.")

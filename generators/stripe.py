"""Generate fake Stripe transaction data linked to credit card data."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

TOKENS = ["tok_visa", "tok_mastercard", "tok_discover"]
INVALID_CARDS = ["4000000000000044", "4000000000000101", "4000000000000028"]


def _build_record(record: dict) -> dict:
    expiry = record["credit_card_expiry_date"]
    parts = expiry.split("-")
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "valid_card": record["credit_card_number"],
        "token": random.choice(TOKENS),
        "invalid_card": random.choice(INVALID_CARDS),
        "month": parts[1] if len(parts) >= 2 else "01",
        "year": parts[0] if len(parts) >= 1 else "2025",
        "ccv": str(random.randint(100, 999)),
        "ccv_amex": str(random.randint(1000, 9999)),
        "user_id": record["user_id"],
        "dt_current_timestamp": timestamp_now(),
    }


def generate(output_dir: str, credit_card_dir: str) -> None:
    current_date = date_today()
    os.makedirs(output_dir, exist_ok=True)

    csv_dir = os.path.join(credit_card_dir, "csv")
    for idx, filename in enumerate(sorted(os.listdir(csv_dir)), start=1):
        if not filename.endswith(".csv"):
            continue
        records = read_file(os.path.join(csv_dir, filename))
        transactions = [_build_record(r) for r in records]
        write_data(transactions, output_dir, "stripe", idx, current_date,
                   root_tag="Transactions", item_tag="Transaction")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "stripe"), os.path.join(base, "credit_card"))

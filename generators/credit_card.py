"""Generate fake credit card data linked to bank user_ids."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

CARD_TYPES = ["visa", "mastercard", "discover", "diners_club", "laser"]


def _random_card_number() -> str:
    return "-".join(str(random.randint(1000, 9999)) for _ in range(4))


def _random_expiry() -> str:
    year = random.randint(2025, 2034)
    month = random.randint(1, 12)
    return f"{year}-{month:02d}-01"


def _build_record(user_id: str) -> dict:
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "credit_card_number": _random_card_number(),
        "credit_card_expiry_date": _random_expiry(),
        "credit_card_type": random.choice(CARD_TYPES),
        "user_id": user_id,
        "dt_current_timestamp": timestamp_now(),
    }


def generate(output_dir: str, bank_dir: str) -> None:
    current_date = date_today()
    os.makedirs(output_dir, exist_ok=True)

    csv_dir = os.path.join(bank_dir, "csv")
    for idx, filename in enumerate(sorted(os.listdir(csv_dir)), start=1):
        if not filename.endswith(".csv"):
            continue
        records = read_file(os.path.join(csv_dir, filename))
        cards = [_build_record(r["user_id"]) for r in records]
        write_data(cards, output_dir, "credit_card", idx, current_date,
                   root_tag="CreditCards", item_tag="CreditCard")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "credit_card"), os.path.join(base, "bank"))

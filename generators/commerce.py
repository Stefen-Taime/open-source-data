"""Generate fake commerce / product data linked to bank user_ids."""

import os
import random

from utils.helpers import random_uuid, timestamp_now, date_today
from utils.io import read_file, write_data

COLORS = ["red", "green", "blue", "yellow", "purple"]
DEPARTMENTS = ["Electronics", "Fashion", "Footwear", "Audio", "Kitchen"]
MATERIALS = ["Plastic", "Metal", "Leather", "Cotton", "Rubber"]
PRODUCT_NAMES = ["Smart TV", "Leather Wallet", "Running Shoes", "Bluetooth Headphones", "Coffee Maker"]


def _build_record(user_id: str) -> dict:
    price = round(random.uniform(50.0, 500.0), 2)
    return {
        "id": random.randint(1000, 9999),
        "color": random.choice(COLORS),
        "department": random.choice(DEPARTMENTS),
        "material": random.choice(MATERIALS),
        "product_name": random.choice(PRODUCT_NAMES),
        "price": price,
        "price_string": f"{price:.2f}",
        "promo_code": f"DISCOUNT{random.randint(10, 99)}",
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
        products = [_build_record(r["user_id"]) for r in records]
        write_data(products, output_dir, "commerce", idx, current_date,
                   root_tag="Products", item_tag="Product")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "commerce"), os.path.join(base, "bank"))

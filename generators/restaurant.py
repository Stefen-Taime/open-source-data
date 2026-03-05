"""Generate fake restaurant data linked to bank user_ids."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

NAMES = ["Sweet Box", "66 BBQ", "Cafe Delight", "Ocean View", "Mountain Retreat"]
TYPES = ["Bar", "Cafe", "Fast Food", "Fine Dining", "Bistro"]
DESCRIPTIONS = [
    "A cozy place with home-style cooking.",
    "Elegant dining with a panoramic ocean view.",
    "Fast and delicious meals for the on-the-go customer.",
    "A perfect place for a romantic evening.",
    "Fresh and healthy food served in a comfortable setting.",
]
REVIEWS = [
    "Excellent food and friendly service!",
    "A bit pricey but totally worth it.",
    "Not the best experience, but the food was okay.",
    "Loved the ambience and the dessert menu.",
    "Great location, but the service could be better.",
]


def _build_record(user_id: str) -> dict:
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "name": random.choice(NAMES),
        "type": random.choice(TYPES),
        "description": random.choice(DESCRIPTIONS),
        "review": random.choice(REVIEWS),
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
        restaurants = [_build_record(r["user_id"]) for r in records]
        write_data(restaurants, output_dir, "restaurant", idx, current_date,
                   root_tag="Restaurants", item_tag="Restaurant")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "restaurant"), os.path.join(base, "bank"))

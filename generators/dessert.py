"""Generate fake dessert data linked to bank user_ids."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

VARIETIES = ["Doughnut", "Cake", "Pudding", "Cheesecake", "Pie", "Cookie"]
TOPPINGS = ["Toffee Bits", "Walnuts", "Granola", "Mocha Drizzle", "Chocolate Chips", "Berry Compote", "Glaze"]
FLAVORS = ["Peanut Butter", "Espresso", "Chocolate", "Butter Pecan", "Cookies 'n Cream", "Cherry"]


def _build_record(user_id: str) -> dict:
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "variety": random.choice(VARIETIES),
        "topping": random.choice(TOPPINGS),
        "flavor": random.choice(FLAVORS),
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
        desserts = [_build_record(r["user_id"]) for r in records]
        write_data(desserts, output_dir, "dessert", idx, current_date,
                   root_tag="Desserts", item_tag="Dessert")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "dessert"), os.path.join(base, "bank"))

"""Generate fake food data linked to bank user_ids."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

DISHES = {
    "Som Tam": "Granny Smith apples mixed with brown sugar and butter filling, in a flaky all-butter crust, with ice cream.",
    "Pizza": "Smoked salmon, poached eggs, diced red onions and Hollandaise sauce on an English muffin. With a side of roasted potatoes.",
    "Pork Sausage Roll": "Two buttermilk waffles, topped with whipped cream and maple syrup, a side of two eggs served any style, and your choice of smoked bacon or smoked ham.",
    "Cheeseburger": "Three eggs with cilantro, tomatoes, onions, avocados and melted Emmental cheese. With a side of roasted potatoes, and your choice of toast or croissant.",
}
INGREDIENTS = ["Feijoa", "Curry Powder", "Pinto Beans", "Tomato"]
MEASUREMENTS = ["1/4 pint", "1/2 gallon", "1/2 cup", "2 tablespoons"]


def _build_record(user_id: str) -> dict:
    dish = random.choice(list(DISHES.keys()))
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "dish": dish,
        "description": DISHES[dish],
        "ingredient": random.choice(INGREDIENTS),
        "measurement": random.choice(MEASUREMENTS),
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
        foods = [_build_record(r["user_id"]) for r in records]
        write_data(foods, output_dir, "food", idx, current_date,
                   root_tag="Foods", item_tag="Food")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "food"), os.path.join(base, "bank"))

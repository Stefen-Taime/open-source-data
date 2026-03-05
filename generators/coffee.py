"""Generate fake coffee data linked to bank user_ids."""

import os
import random

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

BLEND_NAMES = ["American Volcano", "Major Solstice", "The Blend", "Strong Forrester", "Melty America"]
ORIGINS = [
    "Sul Minas, Brazil",
    "Kigeyo Washing Station, Rwanda",
    "Mount Elgon, Uganda",
    "Mattari, Yemen",
    "Granada, Nicaragua",
]
VARIETIES = ["S288", "Pink Bourbon", "Liberica", "Red Bourbon", "Java"]
NOTES = [
    "delicate, coating, sundried tomato, grapefruit, coriander",
    "astringent, tea-like, toast, cacao nibs, barley",
    "bright, velvety, liquorice, red currant, bakers chocolate",
    "astringent, tea-like, green grape, wheat, rubber",
    "mild, coating, cinnamon, dill, dates",
]
INTENSIFIERS = ["soft", "juicy", "deep", "astringent", "pointed"]


def _build_record(user_id: str) -> dict:
    return {
        "blend_name": random.choice(BLEND_NAMES),
        "origin": random.choice(ORIGINS),
        "variety": random.choice(VARIETIES),
        "notes": random.choice(NOTES),
        "intensifier": random.choice(INTENSIFIERS),
        "user_id": user_id,
        "dt_current_timestamp": timestamp_now(),
    }


def generate(output_dir: str, bank_dir: str) -> None:
    """Read bank CSV files and generate matching coffee data."""
    current_date = date_today()
    os.makedirs(output_dir, exist_ok=True)

    csv_dir = os.path.join(bank_dir, "csv")
    for idx, filename in enumerate(sorted(os.listdir(csv_dir)), start=1):
        if not filename.endswith(".csv"):
            continue
        records = read_file(os.path.join(csv_dir, filename))
        coffees = [_build_record(r["user_id"]) for r in records]
        write_data(coffees, output_dir, "coffee", idx, current_date,
                   root_tag="Coffees", item_tag="Coffee")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "coffee"), os.path.join(base, "bank"))

"""Generate fake beer data linked to bank user_ids."""

import os
import random

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data


BRANDS = ["Carlsberg", "Brewdog", "Heineken", "Guinness", "Budweiser"]
NAMES = ["Imperial Stout", "Pale Ale", "Lager", "Pilsner", "Porter"]
STYLES = ["Strong Ale", "Session IPA", "Wheat Beer", "Sour Ale", "Belgian Dubbel"]
HOPS = ["Millennium", "Cascade", "Galaxy", "Saaz", "Mosaic"]
YEASTS = [
    "1388 - Belgian Strong Ale",
    "1056 - American Ale",
    "WLP001 - California Ale",
    "S04 - English Ale",
    "W34/70 - Lager",
]
MALTS = ["Victory", "Pilsner", "Munich", "Caramel", "Chocolate"]


def _build_record(user_id: str) -> dict:
    return {
        "brand": random.choice(BRANDS),
        "name": random.choice(NAMES),
        "style": random.choice(STYLES),
        "hop": random.choice(HOPS),
        "yeast": random.choice(YEASTS),
        "malts": random.choice(MALTS),
        "ibu": f"{random.randint(20, 70)} IBU",
        "alcohol": f"{random.uniform(4.0, 10.0):.1f}%",
        "blg": f"{random.uniform(10.0, 20.0):.1f}\u00b0Blg",
        "user_id": user_id,
        "dt_current_timestamp": timestamp_now(),
    }


def generate(output_dir: str, bank_dir: str) -> None:
    """Read bank CSV files and generate matching beer data."""
    current_date = date_today()
    os.makedirs(output_dir, exist_ok=True)

    csv_dir = os.path.join(bank_dir, "csv")
    for idx, filename in enumerate(sorted(os.listdir(csv_dir)), start=1):
        if not filename.endswith(".csv"):
            continue
        records = read_file(os.path.join(csv_dir, filename))
        beers = [_build_record(r["user_id"]) for r in records]
        write_data(beers, output_dir, "beer", idx, current_date,
                   root_tag="Beers", item_tag="Beer")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "beer"), os.path.join(base, "bank"))

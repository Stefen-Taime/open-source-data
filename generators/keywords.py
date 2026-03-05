"""Generate fake keyword data linked to bank user_ids."""

import json
import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

BASE_KEYWORDS = [
    "independent film", "court", "courtroom drama", "mutant", "marvel comic",
    "detective", "murder", "hip-hop", "terror", "corruption",
    "economic theory", "war on terror",
]


def _random_keywords() -> str:
    keywords = [
        {"id": random.randint(100, 9999), "name": name}
        for name in random.sample(BASE_KEYWORDS, random.randint(1, 3))
    ]
    return json.dumps(keywords)


def _build_record(user_id: str) -> dict:
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "keywords": _random_keywords(),
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
        kw_list = [_build_record(r["user_id"]) for r in records]
        write_data(kw_list, output_dir, "keywords", idx, current_date,
                   root_tag="Keywords", item_tag="Keyword")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "keywords"), os.path.join(base, "bank"))

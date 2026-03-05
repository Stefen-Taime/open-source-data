"""Generate fake computer data linked to bank user_ids."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

PLATFORMS = ["Linux", "macOS", "Windows"]
TYPES = ["workstation", "server"]
OPERATING_SYSTEMS = ["CentOS 8", "Windows 10", "RHEL 7.7", "High Sierra (10.13)", "Ubuntu Desktop 18.04"]
STACKS = ["Windows", "macOS", "Linux", "Ubuntu", "RHEL"]


def _build_record(user_id: str) -> dict:
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "platform": random.choice(PLATFORMS),
        "type": random.choice(TYPES),
        "os": random.choice(OPERATING_SYSTEMS),
        "stack": ", ".join(random.sample(STACKS, 2)),
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
        computers = [_build_record(r["user_id"]) for r in records]
        write_data(computers, output_dir, "computer", idx, current_date,
                   root_tag="Computers", item_tag="Computer")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "computer"), os.path.join(base, "bank"))

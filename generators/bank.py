"""Generate fake bank account data.

This is the *seed* generator: it produces the base `user_id` values that
all other generators reference.
"""

import os
import random
import string
import uuid
from datetime import datetime

from utils.helpers import random_uuid, random_number, timestamp_now, date_today
from utils.io import write_data

# Fictional bank names
BANK_NAMES = [
    "Global Trust Bank",
    "Silverline Financial",
    "Oceanic Capital",
    "Liberty Banking Corp",
    "Pinnacle Funds",
    "Banque du Soleil",
    "Finance Royale",
    "Banco del Futuro",
    "Zhongxin Jinrong",
]


def random_iban() -> str:
    return "IBAN" + random_number(20)


def random_swift_bic() -> str:
    return "SWIFT" + "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
    )


def generate(output_dir: str, num_files: int = 5, records_per_file: int = 10_000) -> None:
    """Generate bank data files (CSV, JSON, XML)."""
    current_date = date_today()
    os.makedirs(output_dir, exist_ok=True)

    for file_id in range(1, num_files + 1):
        records = []
        for i in range(records_per_file):
            record = {
                "id": i + (file_id - 1) * records_per_file,
                "uid": random_uuid(),
                "account_number": random_number(),
                "iban": random_iban(),
                "bank_name": random.choice(BANK_NAMES),
                "routing_number": random_number(),
                "swift_bic": random_swift_bic(),
                "user_id": str(uuid.uuid4()),
                "dt_current_timestamp": timestamp_now(),
            }
            records.append(record)

        write_data(records, output_dir, "bank", file_id, current_date,
                   root_tag="Records", item_tag="Record")


if __name__ == "__main__":
    generate(os.path.join(os.path.dirname(__file__), "..", "data", "bank"))

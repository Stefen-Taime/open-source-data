"""Generate fake device data linked to bank user_ids."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

MANUFACTURERS = {
    "Apple": {"models": ["iPhone 3GS", "iPhone X", "iPhone 11"], "platform": "iOS"},
    "Samsung": {"models": ["Galaxy S10", "Galaxy Note 10"], "platform": "Android"},
    "Google": {"models": ["Pixel 4", "Pixel 5"], "platform": "Android"},
    "HP": {"models": ["EliteBook", "ProBook"], "platform": "Windows"},
    "ASUS": {"models": ["ZenBook", "VivoBook"], "platform": "Windows"},
}


def _build_record(user_id: str) -> dict:
    manufacturer = random.choice(list(MANUFACTURERS.keys()))
    info = MANUFACTURERS[manufacturer]
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "build_number": random.randint(50, 500),
        "manufacturer": manufacturer,
        "model": random.choice(info["models"]),
        "platform": info["platform"],
        "serial_number": "".join(random.choices(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16
        )),
        "version": random.randint(100, 1000),
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
        devices = [_build_record(r["user_id"]) for r in records]
        write_data(devices, output_dir, "device", idx, current_date,
                   root_tag="Devices", item_tag="Device")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "device"), os.path.join(base, "bank"))

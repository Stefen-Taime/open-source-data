"""Generate fake subscription data linked to stripe data."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

PLANS = ["Standard", "Basic", "Platinum", "Gold", "Bronze"]
STATUSES = ["Active", "Idle", "Blocked", "Cancelled"]
PAYMENT_METHODS = ["Google Pay", "Credit Card", "Paypal", "Bitcoins", "Money Transfer", "Alipay"]
SUBSCRIPTION_TERMS = ["Weekly", "Monthly", "Yearly", "Lifetime", "Quinquennal"]
PAYMENT_TERMS = ["Full Subscription", "Monthly Payment", "Payment in Advance", "Pay per Use"]


def _build_record(record: dict) -> dict:
    return {
        "id": record.get("id", random.randint(1000, 9999)),
        "uid": str(uuid.uuid4()),
        "plan": random.choice(PLANS),
        "status": random.choice(STATUSES),
        "payment_method": random.choice(PAYMENT_METHODS),
        "subscription_term": random.choice(SUBSCRIPTION_TERMS),
        "payment_term": random.choice(PAYMENT_TERMS),
        "user_id": record["user_id"],
        "dt_current_timestamp": timestamp_now(),
    }


def generate(output_dir: str, stripe_dir: str) -> None:
    current_date = date_today()
    os.makedirs(output_dir, exist_ok=True)

    csv_dir = os.path.join(stripe_dir, "csv")
    for idx, filename in enumerate(sorted(os.listdir(csv_dir)), start=1):
        if not filename.endswith(".csv"):
            continue
        records = read_file(os.path.join(csv_dir, filename))
        subscriptions = [_build_record(r) for r in records]
        write_data(subscriptions, output_dir, "subscription", idx, current_date,
                   root_tag="Subscriptions", item_tag="Subscription")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "subscription"), os.path.join(base, "stripe"))

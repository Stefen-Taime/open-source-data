"""Generate fake user profile data from credit card and subscription data."""

import os
import random
import uuid
from datetime import datetime

from faker import Faker

from utils.helpers import timestamp_now, date_today
from utils.io import read_all_from_folder, write_csv, write_json, write_xml

fake = Faker()


def _build_user(user_id: str, credit_card_info: dict, subscription_info: dict) -> dict:
    return {
        "id": random.randint(1000, 9999),
        "uid": user_id,
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "avatar": fake.image_url(),
        "gender": random.choice(["Male", "Female", "Other"]),
        "phone_number": fake.phone_number(),
        "social_insurance_number": fake.ssn(),
        "date_of_birth": str(fake.date_of_birth()),
        "employment": str({"title": fake.job(), "key_skill": "Teamwork"}),
        "address": str({
            "city": fake.city(),
            "street_name": fake.street_name(),
            "street_address": fake.street_address(),
            "zip_code": fake.zipcode(),
            "state": fake.state(),
            "country": fake.country(),
            "coordinates": {"lat": float(fake.latitude()), "lng": float(fake.longitude())},
        }),
        "credit_card": str(credit_card_info),
        "subscription": str(subscription_info),
        "dt_current_timestamp": int(datetime.now().timestamp()),
    }


def generate(output_dir: str, credit_card_dir: str, subscription_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    cc_data = read_all_from_folder(os.path.join(credit_card_dir, "csv"))
    sub_data = read_all_from_folder(os.path.join(subscription_dir, "csv"))

    # Index by user_id for fast lookup
    cc_by_uid = {item["user_id"]: item for item in cc_data}
    sub_by_uid = {item["user_id"]: item for item in sub_data}

    all_uids = set(cc_by_uid.keys()) | set(sub_by_uid.keys())

    users = []
    for uid in all_uids:
        cc_info = cc_by_uid.get(uid, {})
        sub_info = sub_by_uid.get(uid, {})
        users.append(_build_user(uid, cc_info, sub_info))

    # Users get a single file per format (not split by index)
    write_csv(users, os.path.join(output_dir, "csv", "users.csv"))
    write_json(users, os.path.join(output_dir, "json", "users.json"))
    write_xml(users, os.path.join(output_dir, "xml", "users.xml"),
              root_tag="Users", item_tag="User")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(
        os.path.join(base, "user"),
        os.path.join(base, "credit_card"),
        os.path.join(base, "subscription"),
    )

"""Generate fake company data linked to bank user_ids."""

import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

BUSINESS_NAMES = [
    "Armstrong, Little and Cartwright",
    "Welch, Hagenes and Halvorson",
    "Smith Inc",
    "Doe Associates",
    "Johnson Corp",
]
SUFFIXES = ["Inc", "LLC", "Group", "PLC", "Ltd"]
INDUSTRIES = ["Investment Management", "Dairy", "Technology", "Education", "Healthcare"]
CATCH_PHRASES = [
    "Seamless innovative synergy",
    "Revolutionary dynamic strategy",
    "Efficient scalable solution",
    "Proactive global mission",
]
BUZZWORDS = ["Blockchain", "AI", "VR", "Synergy", "Big Data"]
BS_STATEMENTS = [
    "enhance interactive platforms",
    "streamline cloud solutions",
    "optimize next-gen technologies",
    "revolutionize integrated markets",
]


def _build_record(user_id: str) -> dict:
    return {
        "id": random.randint(1000, 9999),
        "uid": str(uuid.uuid4()),
        "business_name": random.choice(BUSINESS_NAMES),
        "suffix": random.choice(SUFFIXES),
        "industry": random.choice(INDUSTRIES),
        "catch_phrase": random.choice(CATCH_PHRASES),
        "buzzword": random.choice(BUZZWORDS),
        "bs_company_statement": random.choice(BS_STATEMENTS),
        "employee_identification_number": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
        "duns_number": f"{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "logo": f"https://example.com/fake-logos/{random.randint(1, 10)}.png",
        "type": "Private",
        "phone_number": f"+{random.randint(1, 999)} {random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
        "full_address": f"Suite {random.randint(1, 1000)} {random.randint(100, 99999)} Random Street, SomeCity, SomeCountry",
        "latitude": round(random.uniform(-90.0, 90.0), 6),
        "longitude": round(random.uniform(-180.0, 180.0), 6),
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
        companies = [_build_record(r["user_id"]) for r in records]
        write_data(companies, output_dir, "company", idx, current_date,
                   root_tag="Companies", item_tag="Company")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "company"), os.path.join(base, "bank"))

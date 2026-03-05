#!/usr/bin/env python3
"""Generate all fake datasets.

Usage:
    python generate_all.py            # generate fresh data in data/
    python generate_all.py --clean    # remove existing data first

The generation order respects dependencies:
    bank -> credit_card, movies, and other categories
    credit_card -> stripe
    movies -> ratings
    stripe -> subscription
    credit_card + subscription -> user
"""

import argparse
import os
import shutil
import sys

# Ensure the project root is on sys.path so that `utils` and `generators`
# can be imported regardless of the working directory.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from generators import (  # noqa: E402
    bank,
    beer,
    coffee,
    commerce,
    company,
    computer,
    credit_card,
    dessert,
    device,
    food,
    keywords,
    movies,
    ratings,
    restaurant,
    stripe,
    subscription,
    user,
)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate all fake datasets.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing data directory before generating.",
    )
    args = parser.parse_args()

    if args.clean and os.path.exists(DATA_DIR):
        print(f"Cleaning {DATA_DIR} ...")
        shutil.rmtree(DATA_DIR)

    os.makedirs(DATA_DIR, exist_ok=True)

    def d(name: str) -> str:
        return os.path.join(DATA_DIR, name)

    # ---- Phase 1: seed data (bank) ----
    print("[1/7] Generating bank data ...")
    bank.generate(d("bank"))

    # ---- Phase 2: categories that depend on bank ----
    print("[2/7] Generating bank-dependent categories ...")
    beer.generate(d("beer"), d("bank"))
    coffee.generate(d("coffee"), d("bank"))
    commerce.generate(d("commerce"), d("bank"))
    company.generate(d("company"), d("bank"))
    computer.generate(d("computer"), d("bank"))
    credit_card.generate(d("credit_card"), d("bank"))
    dessert.generate(d("dessert"), d("bank"))
    device.generate(d("device"), d("bank"))
    food.generate(d("food"), d("bank"))
    keywords.generate(d("keywords"), d("bank"))
    movies.generate(d("movies"), d("bank"))
    restaurant.generate(d("restaurant"), d("bank"))

    # ---- Phase 3: stripe (depends on credit_card) ----
    print("[3/7] Generating stripe data ...")
    stripe.generate(d("stripe"), d("credit_card"))

    # ---- Phase 4: ratings (depends on movies) ----
    print("[4/7] Generating ratings data ...")
    ratings.generate(d("ratings"), d("movies"))

    # ---- Phase 5: subscription (depends on stripe) ----
    print("[5/7] Generating subscription data ...")
    subscription.generate(d("subscription"), d("stripe"))

    # ---- Phase 6: user (depends on credit_card + subscription) ----
    print("[6/7] Generating user data ...")
    user.generate(d("user"), d("credit_card"), d("subscription"))

    # ---- Done ----
    print("[7/7] Done! All datasets generated in data/")


if __name__ == "__main__":
    main()

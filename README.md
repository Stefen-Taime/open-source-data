# Open Source Data

Structured fake datasets across 17 categories, available in **CSV**, **JSON**, and **XML** formats. All records are linked by a common `user_id`, making it easy to join data across categories for testing, demos, and data engineering practice.

## Quick start

```bash
# 1. Clone the repository
git clone https://github.com/Stefen-Taime/open-source-data.git
cd open-source-data

# 2. Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate all datasets
python generate_all.py          # generates data/ directory
python generate_all.py --clean  # wipe data/ and regenerate from scratch
```

## Project structure

```
open-source-data/
├── generate_all.py        # Main script: generates all datasets in order
├── requirements.txt       # Python dependencies (faker)
├── generators/            # One module per data category
│   ├── bank.py            # Seed generator (creates base user_ids)
│   ├── beer.py
│   ├── coffee.py
│   ├── commerce.py
│   ├── company.py
│   ├── computer.py
│   ├── credit_card.py
│   ├── dessert.py
│   ├── device.py
│   ├── food.py
│   ├── keywords.py
│   ├── movies.py
│   ├── ratings.py         # Depends on movies
│   ├── restaurant.py
│   ├── stripe.py          # Depends on credit_card
│   ├── subscription.py    # Depends on stripe
│   └── user.py            # Depends on credit_card + subscription
├── utils/                 # Shared utilities
│   ├── io.py              # Read/write CSV, JSON, XML
│   └── helpers.py         # Random data helpers
└── data/                  # Generated datasets (git-ignored)
    ├── bank/
    │   ├── csv/
    │   ├── json/
    │   └── xml/
    ├── beer/
    ├── ...
    └── user/
```

## Data categories

| Category       | Description                        | Depends on     |
| -------------- | ---------------------------------- | -------------- |
| bank           | Fake bank accounts (seed data)     | --             |
| beer           | Beer brands, styles, hops          | bank           |
| coffee         | Coffee blends, origins, varieties  | bank           |
| commerce       | Products, prices, promo codes      | bank           |
| company        | Company profiles, industries       | bank           |
| computer       | Platforms, OS, stacks              | bank           |
| credit_card    | Card numbers, types, expiry dates  | bank           |
| dessert        | Varieties, toppings, flavors       | bank           |
| device         | Manufacturers, models, platforms   | bank           |
| food           | Dishes, ingredients, measurements  | bank           |
| keywords       | Movie-related keyword tags         | bank           |
| movies         | Movie metadata (genres, cast, etc.)| bank           |
| ratings        | User ratings for movies            | movies         |
| restaurant     | Restaurant profiles and reviews    | bank           |
| stripe         | Payment transaction data           | credit_card    |
| subscription   | Subscription plans and statuses    | stripe         |
| user           | User profiles with full details    | credit_card, subscription |

## How it works

1. **`bank.py`** generates seed records with unique `user_id` values.
2. Other generators read the bank CSV data and create domain-specific records for each `user_id`.
3. Some generators have chained dependencies (e.g., `stripe` reads from `credit_card` output).
4. **`user.py`** aggregates credit card and subscription data to build complete user profiles using the [Faker](https://faker.readthedocs.io/) library.

Each category outputs **5 files per format** (100 records each), except `user` which produces a single file per format.

## File naming convention

```
{format}_{category}_{YYYYMMDD}_{index}.{ext}

Examples:
  csv_bank_20260305_1.csv
  json_beer_20260305_3.json
  xml_movies_20260305_5.xml
```

## Reference key

All datasets share a common **`user_id`** field (UUID v4), enabling cross-category joins:

```sql
SELECT u.first_name, b.bank_name, c.blend_name
FROM users u
JOIN bank b ON u.uid = b.user_id
JOIN coffee c ON u.uid = c.user_id;
```

## Contributing

Contributions are welcome. To add a new data category:

1. Create `generators/your_category.py` with a `generate(output_dir, source_dir)` function.
2. Add the call to `generate_all.py` in the appropriate phase.
3. Update this README.

## License

This project is open source and available for educational and development purposes.

## Contact

Stefen Taime -- stefentaime@gmail.com

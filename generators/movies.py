"""Generate fake movie data linked to bank user_ids."""

import json
import os
import random
import uuid

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data

GENRES = [
    {"id": 18, "name": "Drama"},
    {"id": 16, "name": "Animation"},
    {"id": 878, "name": "Science Fiction"},
    {"id": 35, "name": "Comedy"},
    {"id": 10749, "name": "Romance"},
    {"id": 12, "name": "Adventure"},
    {"id": 80, "name": "Crime"},
]
PRODUCTION_COMPANIES = [
    {"name": "D.A. Films", "id": 6541},
    {"name": "Tatsunoko Productions Company", "id": 34037},
    {"name": "Studio Ghibli", "id": 34038},
    {"name": "Warner Bros", "id": 34039},
    {"name": "Pixar Animation Studios", "id": 34040},
]
PRODUCTION_COUNTRIES = [
    {"iso_3166_1": "FR", "name": "France"},
    {"iso_3166_1": "JP", "name": "Japan"},
    {"iso_3166_1": "US", "name": "United States"},
    {"iso_3166_1": "GB", "name": "United Kingdom"},
    {"iso_3166_1": "DE", "name": "Germany"},
]
LANGUAGES = ["fr", "ja", "en", "es", "de"]
OVERVIEWS = [
    "This is a dramatic story of love and adventure.",
    "A thrilling journey of discovery unfolds in this exciting film.",
    "A comedic tale of mishaps and friendship.",
    "An intense drama about the challenges of life and relationships.",
]
STATUSES = ["Released", "Post Production", "In Production"]


def _build_record(user_id: str) -> dict:
    vote_avg = round(random.uniform(0, 10), 1)
    vote_cnt = random.randint(0, 1000)
    year = random.randint(1980, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return {
        "user_id": user_id,
        "adult": random.choice(["True", "False"]),
        "belongs_to_collection": "",
        "genres": json.dumps(random.sample(GENRES, random.randint(1, 3))),
        "id": str(uuid.uuid4()),
        "imdb_id": f"tt{random.randint(1000000, 9999999)}",
        "original_language": random.choice(LANGUAGES),
        "original_title": "Random Movie Title",
        "overview": random.choice(OVERVIEWS),
        "popularity": round(random.uniform(0, 10), 6),
        "production_companies": json.dumps(random.sample(PRODUCTION_COMPANIES, random.randint(1, 2))),
        "production_countries": json.dumps(random.sample(PRODUCTION_COUNTRIES, random.randint(1, 2))),
        "release_date": f"{year}-{month:02d}-{day:02d}",
        "revenue": float(random.randint(0, 1000000)),
        "status": random.choice(STATUSES),
        "title": "Random Movie Title",
        "vote_average": vote_avg,
        "vote_count": vote_cnt,
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
        movies = [_build_record(r["user_id"]) for r in records]
        write_data(movies, output_dir, "movies", idx, current_date,
                   root_tag="Movies", item_tag="Movie")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "movies"), os.path.join(base, "bank"))

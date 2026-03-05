"""Generate fake rating data linked to movie data."""

import os
import random
import time
from datetime import datetime

from utils.helpers import timestamp_now, date_today
from utils.io import read_file, write_data


def _build_record(user_id: str, movie_id: str) -> dict:
    return {
        "user_id": user_id,
        "movieid": movie_id,
        "rating": round(random.uniform(0.5, 5.0), 1),
        "timestamp": int(time.mktime(datetime.now().timetuple())),
        "dt_current_timestamp": timestamp_now(),
    }


def generate(output_dir: str, movies_dir: str) -> None:
    current_date = date_today()
    os.makedirs(output_dir, exist_ok=True)

    csv_dir = os.path.join(movies_dir, "csv")
    for idx, filename in enumerate(sorted(os.listdir(csv_dir)), start=1):
        if not filename.endswith(".csv"):
            continue
        movies = read_file(os.path.join(csv_dir, filename))
        ratings = [_build_record(m["user_id"], m["id"]) for m in movies]
        write_data(ratings, output_dir, "ratings", idx, current_date,
                   root_tag="Ratings", item_tag="Rating")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generate(os.path.join(base, "ratings"), os.path.join(base, "movies"))

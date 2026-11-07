import time
import requests
import json
import os
from datetime import datetime, timezone

import duckdb

LOCATIONS = {
    "saint_john": (45.2733, -66.0633),
    "fredericton": (45.9636, -66.6431),
    "moncton": (46.0878, -64.7782),
    "halifax": (44.6488, -63.5752),
}

URL = "https://api.open-meteo.com/v1/forecast"


def fetch_location(name, lat, lon, retries=3):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "past_days": 7,
        "forecast_days": 1,
        "timezone": "UTC",
    }
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(URL, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            print(f"{name}: attempt {attempt} failed: {error}")
            if attempt == retries:
                raise
            time.sleep(2 ** attempt)
def to_rows(name, lat, lon, data):
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    rows = []
    for t, temp in zip(times, temps):
        rows.append((name, lat, lon, t, temp))
    return rows

def save_raw(name, data):
    os.makedirs("data/raw", exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = f"data/raw/{name}_{stamp}.json"
    with open(path, "w") as f:
        json.dump(data, f)
    return path

def load_rows(rows):
    os.makedirs("data", exist_ok=True)
    con = duckdb.connect("data/warehouse.duckdb")
    con.execute("create schema if not exists raw")
    con.execute("""
        create table if not exists raw.hourly_temperature (
            location varchar,
            latitude double,
            longitude double,
            observed_at varchar,
            temperature_c double,
            loaded_at timestamp
        )
    """)
    loaded_at = datetime.now(timezone.utc).replace(tzinfo=None)
    con.executemany(
        "insert into raw.hourly_temperature values (?, ?, ?, ?, ?, ?)",
        [row + (loaded_at,) for row in rows],
    )
    con.close()


if __name__ == "__main__":
    all_rows = []
    for name, (lat, lon) in LOCATIONS.items():
        data = fetch_location(name, lat, lon)
        save_raw(name, data)
        all_rows.extend(to_rows(name, lat, lon, data))
    load_rows(all_rows)
    print("loaded rows:", len(all_rows))

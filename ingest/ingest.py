import time
import requests

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

if __name__ == "__main__":
    for name, (lat, lon) in LOCATIONS.items():
        data = fetch_location(name, lat, lon)
        rows = to_rows(name, lat, lon, data)
        nulls = sum(1 for r in rows if r[4] is None)
        print(name, "rows:", len(rows), "nulls:", nulls)

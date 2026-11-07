import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 45.2733,
	"longitude": -66.0633,
	"hourly": "temperature_2m",
	"past_days": 7,
	"forecast_days": 1,
	"timezone": "UTC",
}

response = requests.get(url, params=params, timeout=30)
print("status:", response.status_code)

data = response.json()
print("keys:", list(data.keys()))
print("rows:", len(data["hourly"]["time"]))
print("first:", data["hourly"]["time"][0], data["hourly"]["temperature_2m"][0])
print("last:", data["hourly"]["time"][-1], data["hourly"]["temperature_2m"][-1])

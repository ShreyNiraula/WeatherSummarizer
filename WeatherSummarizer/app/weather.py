import requests

# TODO: make location user input? and change timezone as well?
# TODO: change forecast_days variable?
# Open-Meteo API endpoint and parameters
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 34.7304,
    "longitude": -86.5859,
    "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "rain", "wind_speed_10m"],
    "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
    "timezone": "America/Chicago",
    "forecast_days": 1
}

# Function to fetch weather data from Open-Meteo API
def fetch_weather_data():
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()



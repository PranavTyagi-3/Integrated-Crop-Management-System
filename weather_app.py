import requests
from datetime import datetime, timedelta

# Define your API keys
OWM_API_KEY = "5138d66fbb91acdb14176da6d4c2e4e0"
AW_API_KEY = "Mtr00I2Vwpve7zw6egAq94PtDY4y51S9"
TOMORROWIO_API_KEY = "bAqWsK7Zqlw5AcJ7BKHpqZeOCKQGlA9R"

# Define base URLs
OWM_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
AW_BASE_URL = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"
TOMORROWIO_BASE_URL = "https://api.tomorrow.io/v4/weather/forecast"

# Function to get weather forecast from OpenWeatherMap
def fetch_openweathermap_forecast(city_name):
    params = {
        'q': city_name,
        'appid': OWM_API_KEY,
        'units': 'metric'
    }
    response = requests.get(OWM_BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get weather forecast from AccuWeather
def fetch_accuweather_forecast(city_location_key):
    params = {
        'apikey': AW_API_KEY,
        'language': 'en-us',
        'details': 'true'
    }
    response = requests.get(AW_BASE_URL + city_location_key, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get weather forecast from Tomorrow.io
def fetch_tomorrowio_forecast(lat, lon):
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")

    params = {
        'location': f"{lat},{lon}",
        'apikey': TOMORROWIO_API_KEY,
        'timesteps': '1d',
        'startTime': tomorrow,
        'endTime': f"{tomorrow[:10]}T23:59:59Z",
    }

    response = requests.get(TOMORROWIO_BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Helper function to convert Fahrenheit to Celsius
def fahrenheit_to_celsius(f):
    return (f - 32) * (5 / 9)

# Coordinates for Sehore
latitude = 23.1995  # Latitude of Sehore
longitude = 77.0863  # Longitude of Sehore
city_name = "Sehore"
city_location_key = "189094"  # Location key for AccuWeather

# Fetch forecasts from all three providers
owm_data = fetch_openweathermap_forecast(city_name)
aw_data = fetch_accuweather_forecast(city_location_key)
tomorrowio_data = fetch_tomorrowio_forecast(latitude, longitude)

# Display weather information from each provider
if owm_data:
    print("Weather data from OpenWeatherMap:")
    for forecast in owm_data['list']:
        time = forecast['dt_txt']
        temp = forecast['main']['temp']
        humidity = forecast['main']['humidity']
        weather = forecast['weather'][0]['description']

        print(f"Time: {time}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Weather: {weather}")
        print("-" * 20)
else:
    print("Unable to fetch weather data from OpenWeatherMap.")

if aw_data:
    print("\nWeather data from AccuWeather:")
    for forecast in aw_data:
        time = forecast['DateTime']
        temp = fahrenheit_to_celsius(forecast['Temperature']['Value'])
        condition = forecast['IconPhrase']

        print(f"Time: {time}")
        print(f"Temperature: {temp:.2f}°C")
        print(f"Weather Condition: {condition}")
        print("-" * 20)
else:
    print("Unable to fetch weather data from AccuWeather.")

if tomorrowio_data:
    print("\nWeather data from Tomorrow.io:")
    daily_forecast = tomorrowio_data['timelines']['daily'][0]

    temp_max = daily_forecast['values'].get('temperatureMax', 'N/A')
    temp_min = daily_forecast['values'].get('temperatureMin', 'N/A')
    weather_condition = daily_forecast['values'].get('weatherCode', 'Unknown')

    print(f"Max Temperature: {temp_max}°C")
    print(f"Min Temperature: {temp_min}°C")
    print(f"Weather Condition: {weather_condition}")
    print("-" * 20)
else:
    print("Unable to fetch weather data from Tomorrow.io.")

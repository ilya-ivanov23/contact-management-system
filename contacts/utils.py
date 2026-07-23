import requests
from django.core.cache import cache

def get_weather_for_city(city_name):
    if not city_name:
        return None

    normalized_city = city_name.strip().lower()
    cache_key = f"weather_{normalized_city}"

    # 1. Check Django local memory cache
    cached_weather = cache.get(cache_key)
    if cached_weather:
        return cached_weather

    # 2. Cache miss, query OpenStreetMap Nominatim
    geocoding_url = "https://nominatim.openstreetmap.org/search"
    geo_params = {
        'q': city_name,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'ContactsWeatherIntegration/1.0 (contact@example.com)'
    }

    try:
        geo_response = requests.get(geocoding_url, params=geo_params, headers=headers, timeout=5)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            return None

        lat = geo_data[0].get('lat')
        lon = geo_data[0].get('lon')

        # Query Open-Meteo Weather API
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True
        }

        weather_response = requests.get(weather_url, params=weather_params, timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current_weather = weather_data.get('current_weather', {})
        if not current_weather:
            return None

        result = {
            'temperature': current_weather.get('temperature'),
            'windspeed': current_weather.get('windspeed')
        }

        # 3. Store the result in cache for 45 minutes (2700 seconds)
        cache.set(cache_key, result, 2700)

        return result

    except requests.RequestException:
        return None

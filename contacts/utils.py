import requests
from django.core.cache import cache

def get_weather_for_city(city_name):
    if not city_name:
        return None

    normalized_city = city_name.strip().lower()
    cache_key = f"weather_{normalized_city}"

    cached_weather = cache.get(cache_key)
    if cached_weather:
        return cached_weather

    lat, lon = None, None

    # 1. Try Nominatim Geocoding API with a valid User-Agent
    try:
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        geo_params = {'q': city_name, 'format': 'json', 'limit': 1}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ContactsApp/1.0'
        }
        geo_response = requests.get(nominatim_url, params=geo_params, headers=headers, timeout=5)
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            if geo_data:
                lat = geo_data[0].get('lat')
                lon = geo_data[0].get('lon')
    except requests.RequestException:
        pass

    # 2. Fallback to Open-Meteo Geocoding if Nominatim fails
    if not lat or not lon:
        try:
            om_geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            om_params = {'name': city_name, 'count': 1, 'format': 'json'}
            om_response = requests.get(om_geo_url, params=om_params, timeout=5)
            if om_response.status_code == 200:
                results = om_response.json().get('results', [])
                if results:
                    lat = results[0].get('latitude')
                    lon = results[0].get('longitude')
        except requests.RequestException:
            pass

    if not lat or not lon:
        return None

    # 3. Query Open-Meteo Weather API
    try:
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

        # Cache for 45 minutes (2700 seconds)
        cache.set(cache_key, result, 2700)
        return result

    except requests.RequestException:
        return None

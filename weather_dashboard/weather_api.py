"""
Weather API Module
Handles all interactions with OpenWeatherMap API.
"""

import requests
import json
from datetime import datetime, timedelta


class WeatherAPI:
    """Handles weather API requests and data processing"""
    
    def __init__(self, api_key):
        """Initialize with API key"""
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.cache = {}
        self.cache_duration = 600  # 10 minutes in seconds
    
    def _make_request(self, endpoint, params):
        """Make API request with error handling"""
        params['appid'] = self.api_key
        params['units'] = 'metric'  # Use Celsius
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("Error: Invalid API key!")
            elif response.status_code == 404:
                print("Error: City not found!")
            else:
                print(f"Error: Request failed with status {response.status_code}")
            
            return None
            
        except requests.exceptions.Timeout:
            print("Error: Request timed out!")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: No internet connection!")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def _is_cache_valid(self, cache_key):
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key]['timestamp']
        current_time = datetime.now()
        
        time_diff = (current_time - cached_time).total_seconds()
        
        return time_diff < self.cache_duration
    
    def get_current_weather(self, city):
        """Get current weather for a city"""
        cache_key = f"current_{city.lower()}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            print("(Using cached data)")
            return self.cache[cache_key]['data']
        
        params = {'q': city}
        data = self._make_request('weather', params)
        
        if not data:
            return None
        
        # Parse and format the response
        weather_info = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'], 1)
        }
        
        # Cache the result
        self.cache[cache_key] = {
            'data': weather_info,
            'timestamp': datetime.now()
        }
        
        return weather_info
    
    def get_forecast(self, city):
        """Get 5-day forecast for a city"""
        cache_key = f"forecast_{city.lower()}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            print("(Using cached data)")
            return self.cache[cache_key]['data']
        
        params = {'q': city}
        data = self._make_request('forecast', params)
        
        if not data:
            return None
        
        # Process forecast data (get one forecast per day at noon)
        forecasts = []
        processed_dates = set()
        
        for item in data['list']:
            date_time = datetime.fromtimestamp(item['dt'])
            date_str = date_time.strftime('%Y-%m-%d')
            
            # Get forecast around noon (12:00)
            if date_str not in processed_dates and date_time.hour == 12:
                forecast = {
                    'date': date_time.strftime('%A, %B %d'),
                    'temp_min': round(item['main']['temp_min'], 1),
                    'temp_max': round(item['main']['temp_max'], 1),
                    'description': item['weather'][0]['description'],
                    'humidity': item['main']['humidity']
                }
                forecasts.append(forecast)
                processed_dates.add(date_str)
            
            if len(forecasts) >= 5:
                break
        
        forecast_info = {
            'city': data['city']['name'],
            'forecasts': forecasts
        }
        
        # Cache the result
        self.cache[cache_key] = {
            'data': forecast_info,
            'timestamp': datetime.now()
        }
        
        return forecast_info
    
    def clear_cache(self):
        """Clear the cache"""
        self.cache = {}
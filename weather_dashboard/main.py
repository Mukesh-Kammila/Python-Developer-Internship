"""
Weather Information Dashboard - Main Application
Displays weather information for different cities.
"""

from weather_api import WeatherAPI
from data_storage import DataStorage
import sys


def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("     WEATHER INFORMATION DASHBOARD")
    print("="*50)
    print("1. Get Current Weather")
    print("2. Get 5-Day Forecast")
    print("3. View Saved Locations")
    print("4. Add Favorite Location")
    print("5. Remove Favorite Location")
    print("6. Exit")
    print("="*50)


def display_current_weather(weather_data):
    """Display current weather information"""
    if not weather_data:
        print("Could not retrieve weather data!")
        return
    
    print("\n" + "="*50)
    print(f"   Weather in {weather_data['city']}, {weather_data['country']}")
    print("="*50)
    print(f"\nTemperature: {weather_data['temperature']}°C")
    print(f"Feels Like: {weather_data['feels_like']}°C")
    print(f"Condition: {weather_data['description'].title()}")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Wind Speed: {weather_data['wind_speed']} m/s")
    print(f"Pressure: {weather_data['pressure']} hPa")
    print("="*50)


def display_forecast(forecast_data):
    """Display 5-day forecast"""
    if not forecast_data:
        print("Could not retrieve forecast data!")
        return
    
    print("\n" + "="*50)
    print(f"   5-Day Forecast for {forecast_data['city']}")
    print("="*50)
    
    for day in forecast_data['forecasts']:
        print(f"\n{day['date']}")
        print(f"  Temperature: {day['temp_min']}°C - {day['temp_max']}°C")
        print(f"  Condition: {day['description'].title()}")
        print(f"  Humidity: {day['humidity']}%")
        print("-" * 50)


def get_weather(api, storage):
    """Get current weather for a city"""
    city = input("\nEnter city name: ").strip()
    
    if not city:
        print("City name cannot be empty!")
        return
    
    print("\nFetching weather data...")
    weather_data = api.get_current_weather(city)
    
    if weather_data:
        display_current_weather(weather_data)
        
        # Ask if user wants to save this location
        save = input("\nSave this location to favorites? (y/n): ").strip().lower()
        if save == 'y':
            if storage.add_favorite(city):
                print(f"✓ {city} added to favorites!")
            else:
                print(f"✗ {city} is already in favorites!")
    else:
        print(f"✗ Could not find weather data for '{city}'")


def get_forecast(api):
    """Get 5-day forecast for a city"""
    city = input("\nEnter city name: ").strip()
    
    if not city:
        print("City name cannot be empty!")
        return
    
    print("\nFetching forecast data...")
    forecast_data = api.get_forecast(city)
    
    if forecast_data:
        display_forecast(forecast_data)
    else:
        print(f"✗ Could not find forecast data for '{city}'")


def view_favorites(storage, api):
    """View and select from saved locations"""
    favorites = storage.get_favorites()
    
    if not favorites:
        print("\nNo favorite locations saved yet!")
        return
    
    print("\n--- Favorite Locations ---")
    for i, city in enumerate(favorites, 1):
        print(f"{i}. {city}")
    
    choice = input("\nEnter number to view weather (or press Enter to go back): ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(favorites):
            city = favorites[idx]
            print(f"\nFetching weather for {city}...")
            weather_data = api.get_current_weather(city)
            if weather_data:
                display_current_weather(weather_data)


def add_favorite(storage):
    """Add a city to favorites"""
    city = input("\nEnter city name to add: ").strip()
    
    if not city:
        print("City name cannot be empty!")
        return
    
    if storage.add_favorite(city):
        print(f"✓ {city} added to favorites!")
    else:
        print(f"✗ {city} is already in favorites!")


def remove_favorite(storage):
    """Remove a city from favorites"""
    favorites = storage.get_favorites()
    
    if not favorites:
        print("\nNo favorite locations to remove!")
        return
    
    print("\n--- Favorite Locations ---")
    for i, city in enumerate(favorites, 1):
        print(f"{i}. {city}")
    
    choice = input("\nEnter number to remove (or press Enter to cancel): ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(favorites):
            city = favorites[idx]
            if storage.remove_favorite(city):
                print(f"✓ {city} removed from favorites!")


def main():
    """Main application loop"""
    # Note: Replace 'your_api_key_here' with actual OpenWeatherMap API key
    api_key = "your_api_key_here"
    
    api = WeatherAPI(api_key)
    storage = DataStorage()
    
    print("\nWelcome to Weather Information Dashboard!")
    print("Note: You need a valid OpenWeatherMap API key to use this application.")
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            get_weather(api, storage)
        
        elif choice == '2':
            get_forecast(api)
        
        elif choice == '3':
            view_favorites(storage, api)
        
        elif choice == '4':
            add_favorite(storage)
        
        elif choice == '5':
            remove_favorite(storage)
        
        elif choice == '6':
            print("\nThank you for using Weather Dashboard!")
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print("\n✗ Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
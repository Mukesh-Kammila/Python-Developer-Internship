"""
Data Storage Module
Manages local storage of favorite cities and preferences.
"""

import json
import os


class DataStorage:
    """Handles local data storage operations"""
    
    def __init__(self, filename='weather_data.json'):
        """Initialize data storage"""
        self.filename = filename
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from JSON file"""
        if not os.path.exists(self.filename):
            # Create default data structure
            default_data = {
                'favorites': [],
                'settings': {
                    'units': 'metric',
                    'default_city': None
                }
            }
            self._save_data(default_data)
            return default_data
        
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError:
            print("Error: Corrupted data file. Creating new one.")
            default_data = {'favorites': [], 'settings': {}}
            self._save_data(default_data)
            return default_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return {'favorites': [], 'settings': {}}
    
    def _save_data(self, data=None):
        """Save data to JSON file"""
        if data is None:
            data = self.data
        
        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def get_favorites(self):
        """Get list of favorite cities"""
        return self.data.get('favorites', [])
    
    def add_favorite(self, city):
        """Add a city to favorites"""
        city = city.strip().title()
        
        favorites = self.data.get('favorites', [])
        
        if city in favorites:
            return False
        
        favorites.append(city)
        self.data['favorites'] = favorites
        
        return self._save_data()
    
    def remove_favorite(self, city):
        """Remove a city from favorites"""
        city = city.strip().title()
        
        favorites = self.data.get('favorites', [])
        
        if city not in favorites:
            return False
        
        favorites.remove(city)
        self.data['favorites'] = favorites
        
        return self._save_data()
    
    def is_favorite(self, city):
        """Check if a city is in favorites"""
        city = city.strip().title()
        return city in self.data.get('favorites', [])
    
    def get_setting(self, key, default=None):
        """Get a setting value"""
        return self.data.get('settings', {}).get(key, default)
    
    def set_setting(self, key, value):
        """Set a setting value"""
        if 'settings' not in self.data:
            self.data['settings'] = {}
        
        self.data['settings'][key] = value
        return self._save_data()
    
    def get_default_city(self):
        """Get default city"""
        return self.data.get('settings', {}).get('default_city')
    
    def set_default_city(self, city):
        """Set default city"""
        city = city.strip().title()
        return self.set_setting('default_city', city)
    
    def clear_favorites(self):
        """Clear all favorites"""
        self.data['favorites'] = []
        return self._save_data()
    
    def export_favorites(self, filename='favorites_export.txt'):
        """Export favorites to text file"""
        favorites = self.get_favorites()
        
        if not favorites:
            print("No favorites to export!")
            return False
        
        try:
            with open(filename, 'w') as file:
                file.write("FAVORITE CITIES\n")
                file.write("=" * 30 + "\n\n")
                for i, city in enumerate(favorites, 1):
                    file.write(f"{i}. {city}\n")
            print(f"✓ Favorites exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting: {e}")
            return False
    
    def get_data_summary(self):
        """Get summary of stored data"""
        return {
            'total_favorites': len(self.data.get('favorites', [])),
            'default_city': self.get_default_city(),
            'units': self.get_setting('units', 'metric')
        }
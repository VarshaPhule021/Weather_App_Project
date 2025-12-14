"""
Data Models for Weather App
Defines User, Weather, and Forecast data structures
"""

from datetime import datetime
from typing import Dict, Optional, List


class User:
    """User Model - Represents a user account"""
    
    def __init__(self, email: str, username: str, password: str, created_at: Optional[str] = None):
        """
        Initialize User instance
        
        Args:
            email: User email address (unique identifier)
            username: User display name
            password: User password (should be hashed in production)
            created_at: Account creation timestamp
        """
        self.email = email
        self.username = username
        self.password = password
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary for storage"""
        return {
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(email: str, data: Dict) -> 'User':
        """Create User instance from dictionary"""
        return User(
            email=email,
            username=data['username'],
            password=data['password'],
            created_at=data.get('created_at')
        )
    
    def __repr__(self) -> str:
        return f"User(email={self.email}, username={self.username})"


class WeatherData:
    """Weather Model - Represents current weather information"""
    
    def __init__(self, data: Dict):
        """
        Initialize weather data from API response
        
        Args:
            data: Dictionary containing raw weather data from OpenWeather API
        """
        try:
            self.city = data.get('name', 'Unknown')
            self.country = data.get('sys', {}).get('country', 'N/A')
            self.latitude = round(data.get('coord', {}).get('lat', 0), 4)
            self.longitude = round(data.get('coord', {}).get('lon', 0), 4)
            
            # Condition
            weather_data = data.get('weather', [{}])[0]
            self.main_condition = weather_data.get('main', 'Clear')
            self.description = weather_data.get('description', '').title()
            self.icon = weather_data.get('icon', '01d')
            
            # Temperature
            main_data = data.get('main', {})
            self.temperature = round(main_data.get('temp', 0), 1)
            self.feels_like = round(main_data.get('feels_like', 0), 1)
            self.temp_min = round(main_data.get('temp_min', 0), 1)
            self.temp_max = round(main_data.get('temp_max', 0), 1)
            
            # Humidity and Pressure
            self.humidity = main_data.get('humidity', 0)
            self.pressure = main_data.get('pressure', 0)
            visibility = data.get('visibility', 0)
            self.visibility = round(visibility / 1000, 1) if visibility > 0 else 0
            
            # Wind
            wind_data = data.get('wind', {})
            self.wind_speed = round(wind_data.get('speed', 0), 1)
            self.wind_deg = wind_data.get('deg', 0)
            self.wind_gust = round(wind_data.get('gust', 0), 1)
            
            # Other
            self.cloudiness = data.get('clouds', {}).get('all', 0)
            
            # Handle sunrise/sunset with proper error handling
            sys_data = data.get('sys', {})
            sunrise_ts = sys_data.get('sunrise', 0)
            sunset_ts = sys_data.get('sunset', 0)
            
            try:
                self.sunrise = datetime.fromtimestamp(sunrise_ts).strftime('%I:%M %p') if sunrise_ts else 'N/A'
                self.sunset = datetime.fromtimestamp(sunset_ts).strftime('%I:%M %p') if sunset_ts else 'N/A'
            except (OSError, ValueError) as e:
                self.sunrise = 'N/A'
                self.sunset = 'N/A'
            
            self.timezone = data.get('timezone', 0)
            self.rain = round(data.get('rain', {}).get('1h', 0), 1)
            self.snow = round(data.get('snow', {}).get('1h', 0), 1)
            self.wind_direction = None  # Will be set by WeatherService
        
        except Exception as e:
            raise ValueError(f"Error initializing WeatherData: {e}")
    
    def to_dict(self) -> Dict:
        """Convert weather data to dictionary for template rendering"""
        return {
            'city': self.city,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'main_condition': self.main_condition,
            'description': self.description,
            'icon': self.icon,
            'temperature': self.temperature,
            'feels_like': self.feels_like,
            'temp_min': self.temp_min,
            'temp_max': self.temp_max,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'visibility': self.visibility,
            'wind_speed': self.wind_speed,
            'wind_deg': self.wind_deg,
            'wind_gust': self.wind_gust,
            'wind_direction': self.wind_direction,
            'cloudiness': self.cloudiness,
            'sunrise': self.sunrise,
            'sunset': self.sunset,
            'timezone': self.timezone,
            'rain': self.rain,
            'snow': self.snow
        }
    
    def __repr__(self) -> str:
        return f"WeatherData({self.city}, {self.country})"


class ForecastDay:
    """Forecast Model - Represents a single day forecast"""
    
    def __init__(self, date: str, day: str, forecast_data: Dict):
        """
        Initialize forecast data for a single day
        
        Args:
            date: Date in YYYY-MM-DD format
            day: Day name (e.g., 'Monday')
            forecast_data: Dictionary with forecast details
        """
        self.date = date
        self.day = day
        self.temp_max = round(forecast_data.get('temp_max', 0), 1)
        self.temp_min = round(forecast_data.get('temp_min', 0), 1)
        self.temp = round(forecast_data.get('temp', 0), 1)
        self.humidity = forecast_data.get('humidity', 0)
        self.description = forecast_data.get('description', '')
        self.icon = forecast_data.get('icon', '')
        self.wind_speed = round(forecast_data.get('wind_speed', 0), 1)
        self.rain_chance = round(forecast_data.get('rain_chance', 0), 0)
    
    def to_dict(self) -> Dict:
        """Convert forecast to dictionary"""
        return {
            'date': self.date,
            'day': self.day,
            'temp_max': self.temp_max,
            'temp_min': self.temp_min,
            'temp': self.temp,
            'humidity': self.humidity,
            'description': self.description,
            'icon': self.icon,
            'wind_speed': self.wind_speed,
            'rain_chance': self.rain_chance
        }
    
    def __repr__(self) -> str:
        return f"ForecastDay({self.date}, {self.day})"


class Session:
    """Session Model - Represents user session"""
    
    def __init__(self, user_email: str, username: str):
        """
        Initialize user session
        
        Args:
            user_email: User's email address
            username: User's username
        """
        self.user_email = user_email
        self.username = username
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def update_activity(self) -> None:
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def __repr__(self) -> str:
        return f"Session(user={self.user_email}, created={self.created_at})"

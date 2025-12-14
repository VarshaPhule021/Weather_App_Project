"""
Service Layer for Weather App
Handles business logic for user management, authentication, and weather operations
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from models import User, WeatherData, ForecastDay
from utils.app_logger import logger


class UserService:
    """Service for user authentication and management"""
    
    USERS_FILE = 'users.json'
    
    def __init__(self):
        """Initialize UserService"""
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """
        Load users from JSON file
        
        Returns:
            Dictionary of users with email as key
        """
        try:
            if os.path.exists(self.USERS_FILE):
                with open(self.USERS_FILE, 'r') as f:
                    logger.info(f"Loading users from {self.USERS_FILE}")
                    return json.load(f)
            logger.info("Users file does not exist, returning empty dict")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {self.USERS_FILE}: {e}")
            return {}
        except IOError as e:
            logger.error(f"IO Error reading {self.USERS_FILE}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error loading users: {e}")
            return {}
    
    def _save_users(self) -> None:
        """Save users to JSON file"""
        try:
            with open(self.USERS_FILE, 'w') as f:
                json.dump(self.users, f, indent=4)
                logger.info(f"Users successfully saved to {self.USERS_FILE}")
        except IOError as e:
            logger.error(f"IO Error writing to {self.USERS_FILE}: {e}")
            raise
        except json.JSONEncodeError as e:
            logger.error(f"Error encoding users to JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error saving users: {e}")
            raise
    
    def register_user(self, email: str, username: str, password: str) -> bool:
        """
        Register a new user
        
        Args:
            email: User email (must be unique)
            username: User display name
            password: User password
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Validation
            if not all([email, username, password]):
                logger.warning("Registration attempt with missing fields")
                return False
            
            if email in self.users:
                logger.warning(f"Registration attempt with existing email: {email}")
                return False
            
            if len(password) < 6:
                logger.warning(f"Registration attempt with weak password for email: {email}")
                return False
            
            # Create new user
            user = User(email, username, password)
            self.users[email] = user.to_dict()
            self._save_users()
            
            logger.info(f"New user registered successfully: {email}")
            return True
        
        except Exception as e:
            logger.error(f"Error registering user {email}: {e}")
            raise
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        try:
            if not email or not password:
                logger.warning("Authentication attempt with missing credentials")
                return None
            
            logger.debug(f"Authentication attempt for email: {email}")
            
            if email not in self.users:
                logger.warning(f"Authentication failed: user not found - {email}")
                return None
            
            user_data = self.users[email]
            
            # Simple password comparison (use hashing in production)
            if user_data['password'] == password:
                logger.info(f"Successful authentication for user: {email}")
                return User.from_dict(email, user_data)
            else:
                logger.warning(f"Failed authentication: invalid password for - {email}")
                return None
        
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            return None
    
    def user_exists(self, email: str) -> bool:
        """Check if user exists"""
        return email in self.users
    
    def get_user(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            if email in self.users:
                return User.from_dict(email, self.users[email])
            return None
        except Exception as e:
            logger.error(f"Error getting user {email}: {e}")
            return None


class WeatherService:
    """Service for weather data fetching and processing"""
    
    CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
    REQUEST_TIMEOUT = 10
    
    def __init__(self, api_key: str):
        """
        Initialize WeatherService
        
        Args:
            api_key: OpenWeather API key
        """
        self.api_key = api_key
    
    def _get_wind_direction(self, degrees: float) -> str:
        """
        Convert wind degrees to compass direction
        
        Args:
            degrees: Wind direction in degrees (0-360)
            
        Returns:
            Compass direction (N, NNE, NE, etc.)
        """
        try:
            directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                         'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            index = round(degrees / 22.5) % 16
            logger.debug(f"Converting {degrees}° to wind direction: {directions[index]}")
            return directions[index]
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting wind direction for degrees {degrees}: {e}")
            return 'N'
        except Exception as e:
            logger.error(f"Unexpected error in get_wind_direction: {e}")
            return 'N'
    
    def get_current_weather(self, city: str) -> Optional[WeatherData]:
        """
        Fetch current weather for a city
        
        Args:
            city: City name
            
        Returns:
            WeatherData object if successful, None otherwise
        """
        try:
            logger.info(f"Fetching weather data for city: {city}")
            
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            try:
                response = requests.get(
                    self.CURRENT_WEATHER_URL,
                    params=params,
                    timeout=self.REQUEST_TIMEOUT
                )
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.Timeout:
                logger.error(f"Timeout error fetching weather for city: {city}")
                return None
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error fetching weather for city: {city} - {e}")
                return None
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error fetching weather for city: {city} - {e}")
                return None
            
            # Handle both string and integer cod values
            cod = data.get('cod')
            if str(cod) != '200':
                logger.warning(f"City not found: {city}. API Response code: {cod}")
                return None
            
            try:
                # Create WeatherData object
                weather = WeatherData(data)
                weather.wind_direction = self._get_wind_direction(weather.wind_deg)
            except (KeyError, TypeError, ValueError) as e:
                logger.error(f"Error creating WeatherData object for {city}: {e}")
                return None
            
            logger.debug(f"Successfully extracted weather data for {weather.city}, {weather.country}")
            return weather
        
        except Exception as e:
            logger.error(f"Unexpected error fetching weather for city {city}: {e}")
            return None
    
    def get_forecast(self, city: str) -> Optional[List[ForecastDay]]:
        """
        Fetch 5-day forecast for a city
        
        Args:
            city: City name
            
        Returns:
            List of ForecastDay objects if successful, None otherwise
        """
        try:
            logger.info(f"Fetching 5-day forecast for city: {city}")
            
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            try:
                response = requests.get(
                    self.FORECAST_URL,
                    params=params,
                    timeout=self.REQUEST_TIMEOUT
                )
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.Timeout:
                logger.error(f"Timeout error fetching forecast for city: {city}")
                return None
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error fetching forecast for city: {city} - {e}")
                return None
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error fetching forecast for city: {city} - {e}")
                return None
            
            # Handle both string and integer cod values
            cod = data.get('cod')
            if str(cod) != '200':
                logger.warning(f"City not found in forecast: {city}. API Response code: {cod}")
                return None
            
            # Process forecast data
            forecast_list = data.get('list', [])
            if not forecast_list:
                logger.warning(f"No forecast data available for {city}")
                return None
                
            daily_forecasts = {}
            
            for forecast in forecast_list:
                try:
                    dt = datetime.fromtimestamp(forecast['dt'])
                    date_key = dt.strftime('%Y-%m-%d')
                    day_name = dt.strftime('%A')
                    
                    # Store forecast data for each day
                    if date_key not in daily_forecasts:
                        daily_forecasts[date_key] = {
                            'day': day_name,
                            'temp_max': forecast['main'].get('temp_max', 0),
                            'temp_min': forecast['main'].get('temp_min', 0),
                            'temp': forecast['main'].get('temp', 0),
                            'humidity': forecast['main'].get('humidity', 0),
                            'description': forecast['weather'][0].get('description', '').title() if forecast.get('weather') else 'N/A',
                            'icon': forecast['weather'][0].get('icon', '') if forecast.get('weather') else '',
                            'wind_speed': forecast['wind'].get('speed', 0),
                            'rain_chance': round((forecast.get('pop', 0) * 100), 1),
                        }
                    else:
                        # Update with max/min values
                        if forecast['main'].get('temp_max', 0) > daily_forecasts[date_key]['temp_max']:
                            daily_forecasts[date_key]['temp_max'] = forecast['main'].get('temp_max', 0)
                        if forecast['main'].get('temp_min', 0) < daily_forecasts[date_key]['temp_min']:
                            daily_forecasts[date_key]['temp_min'] = forecast['main'].get('temp_min', 0)
                except (KeyError, ValueError, TypeError) as e:
                    logger.warning(f"Error processing forecast item: {e}, skipping")
                    continue
                except Exception as e:
                    logger.warning(f"Unexpected error processing forecast item: {e}, skipping")
                    continue
            
            if not daily_forecasts:
                logger.warning(f"No valid forecast data available for {city}")
                return None
            
            # Create ForecastDay objects and return first 5 days
            result = []
            for date_key in list(daily_forecasts.keys())[:5]:
                forecast_data = daily_forecasts[date_key]
                try:
                    forecast_day = ForecastDay(date_key, forecast_data['day'], forecast_data)
                    result.append(forecast_day)
                except Exception as e:
                    logger.warning(f"Error creating ForecastDay object for {date_key}: {e}")
                    continue
            
            logger.info(f"Successfully fetched forecast with {len(result)} days for {city}")
            return result
        
        except Exception as e:
            logger.error(f"Unexpected error fetching forecast for city {city}: {e}")
            return None

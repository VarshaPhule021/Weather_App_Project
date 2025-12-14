from flask import Flask, render_template, request, redirect, url_for, session
from constant.header import API_KEY
from utils.app_logger import logger
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# File to store user data (in production, use a database)
USERS_FILE = 'users.json'

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                logger.info(f"Loading users from {USERS_FILE}")
                return json.load(f)
        logger.info("Users file does not exist, returning empty dict")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {USERS_FILE}: {e}")
        return {}
    except IOError as e:
        logger.error(f"IO Error reading {USERS_FILE}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading users: {e}")
        return {}

def save_users(users):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
            logger.info(f"Users successfully saved to {USERS_FILE}")
    except IOError as e:
        logger.error(f"IO Error writing to {USERS_FILE}: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error encoding users to JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving users: {e}")
        raise

def extract_weather_data(data):
    """Extract comprehensive weather data from API response"""
    try:
        logger.debug(f"Extracting weather data for {data['name']}, {data['sys']['country']}")
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'latitude': round(data['coord']['lat'], 4),
            'longitude': round(data['coord']['lon'], 4),
            'main_condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'temp_min': round(data['main']['temp_min'], 1),
            'temp_max': round(data['main']['temp_max'], 1),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'visibility': round(data['visibility'] / 1000, 1),
            'wind_speed': round(data['wind']['speed'], 1),
            'wind_deg': data['wind'].get('deg', 0),
            'wind_gust': round(data['wind'].get('gust', 0), 1),
            'cloudiness': data['clouds']['all'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p'),
            'timezone': data['timezone'],
            'rain': round(data.get('rain', {}).get('1h', 0), 1),
            'snow': round(data.get('snow', {}).get('1h', 0), 1)
        }
    except KeyError as e:
        logger.error(f"Missing key in weather data: {e}")
        raise ValueError(f"Invalid weather data structure: missing {e}")
    except (ValueError, TypeError) as e:
        logger.error(f"Error processing weather data: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error extracting weather data: {e}")
        raise

def get_wind_direction(degrees):
    """Convert wind degrees to direction"""
    try:
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                      'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        logger.debug(f"Converting {degrees} degrees to wind direction: {directions[index]}")
        return directions[index]
    except (ValueError, TypeError) as e:
        logger.error(f"Error converting wind direction for degrees {degrees}: {e}")
        return 'N'  # Default to North on error
    except Exception as e:
        logger.error(f"Unexpected error in get_wind_direction: {e}")
        return 'N'

def extract_forecast_data(data):
    """Extract 5-day forecast data from API response"""
    try:
        logger.debug("Extracting 5-day forecast data")
        forecast_list = data['list']
        daily_forecasts = {}
        
        for forecast in forecast_list:
            try:
                # Get date in YYYY-MM-DD format
                dt = datetime.fromtimestamp(forecast['dt'])
                date_key = dt.strftime('%Y-%m-%d')
                day_name = dt.strftime('%A')
                
                # Store only the first forecast for each day (at noon)
                if date_key not in daily_forecasts:
                    daily_forecasts[date_key] = {
                        'date': date_key,
                        'day': day_name,
                        'temp_max': round(forecast['main']['temp_max'], 1),
                        'temp_min': round(forecast['main']['temp_min'], 1),
                        'temp': round(forecast['main']['temp'], 1),
                        'humidity': forecast['main']['humidity'],
                        'description': forecast['weather'][0]['description'].title(),
                        'icon': forecast['weather'][0]['icon'],
                        'wind_speed': round(forecast['wind']['speed'], 1),
                        'rain_chance': round(forecast['pop'] * 100, 0),  # Probability of precipitation
                    }
            except KeyError as e:
                logger.warning(f"Missing key in forecast item: {e}, skipping item")
                continue
            except Exception as e:
                logger.warning(f"Error processing forecast item: {e}, skipping item")
                continue
        
        logger.info(f"Successfully extracted {len(daily_forecasts)} days of forecast data")
        # Return only the next 5 days
        return list(daily_forecasts.values())[:5]
    except KeyError as e:
        logger.error(f"Missing key in forecast data structure: {e}")
        raise ValueError(f"Invalid forecast data structure: missing {e}")
    except Exception as e:
        logger.error(f"Unexpected error extracting forecast data: {e}")
        raise

@app.route('/')
def home():
    """Redirect to login if not authenticated"""
    try:
        if 'user' in session:
            logger.info(f"User {session.get('user')} accessing home, redirecting to weather")
            return redirect(url_for('index'))
        logger.debug("Anonymous user accessing home, redirecting to login")
        return redirect(url_for('login'))
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    try:
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            if not email or not password:
                logger.warning("Login attempt with missing email or password")
                error = "Email and password are required!"
                return render_template('login.html', error=error)
            
            logger.debug(f"Login attempt for email: {email}")
            users = load_users()
            
            # Check if user exists and password is correct
            if email in users and users[email]['password'] == password:
                session['user'] = email
                session['username'] = users[email]['username']
                logger.info(f"Successful login for user: {email}")
                return redirect(url_for('index'))
            else:
                logger.warning(f"Failed login attempt for email: {email}")
                error = "Invalid email or password!"
                return render_template('login.html', error=error)
        
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Unexpected error in login route: {e}")
        error = "An error occurred during login. Please try again."
        return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup"""
    try:
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validation
            if not all([username, email, password, confirm_password]):
                logger.warning("Signup attempt with missing fields")
                error = "All fields are required!"
                return render_template('signup.html', error=error)
            
            if password != confirm_password:
                logger.warning(f"Signup attempt with mismatched passwords for email: {email}")
                error = "Passwords do not match!"
                return render_template('signup.html', error=error)
            
            if len(password) < 6:
                logger.warning(f"Signup attempt with weak password for email: {email}")
                error = "Password must be at least 6 characters!"
                return render_template('signup.html', error=error)
            
            users = load_users()
            
            if email in users:
                logger.warning(f"Signup attempt with existing email: {email}")
                error = "Email already registered!"
                return render_template('signup.html', error=error)
            
            # Register new user
            users[email] = {
                'username': username,
                'password': password,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_users(users)
            logger.info(f"New user registered successfully: {email}")
            
            success = "Account created successfully! Please login."
            return render_template('signup.html', success=success)
        
        return render_template('signup.html')
    except Exception as e:
        logger.error(f"Unexpected error in signup route: {e}")
        error = "An error occurred during signup. Please try again."
        return render_template('signup.html', error=error)

@app.route('/logout')
def logout():
    """Handle user logout"""
    try:
        user = session.get('user', 'Unknown')
        logger.info(f"User {user} logging out")
        session.clear()
        return redirect(url_for('login'))
    except Exception as e:
        logger.error(f"Error in logout route: {e}")
        return redirect(url_for('login'))

@app.route('/forecast', methods=['GET'])
def forecast():
    """Display 5-day forecast page - requires login"""
    if 'user' not in session:
        logger.warning("Unauthenticated user attempting to access forecast page")
        return redirect(url_for('login'))
    
    try:
        city = request.args.get('city', '').strip()
        
        if not city:
            logger.warning(f"Forecast request from {session.get('user')} without city parameter")
            error = "City not specified!"
            return render_template('index.html', error=error, username=session.get('username'))
        
        logger.info(f"Fetching 5-day forecast for city: {city}")
        
        # Fetch 5-day forecast
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        try:
            forecast_response = requests.get(forecast_url, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error fetching forecast for city: {city}")
            error = "Request timeout. Please try again."
            return render_template('index.html', error=error, username=session.get('username'))
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching forecast for city: {city} - {e}")
            error = "Could not fetch forecast data from API."
            return render_template('index.html', error=error, username=session.get('username'))
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching forecast for city: {city} - {e}")
            error = "Network error occurred. Please check your connection."
            return render_template('index.html', error=error, username=session.get('username'))
        
        if forecast_data.get('cod') == '200':
            try:
                forecast_list = extract_forecast_data(forecast_data)
                city_name = forecast_data['city']['name']
                country = forecast_data['city']['country']
                latitude = round(forecast_data['city']['coord']['lat'], 4)
                longitude = round(forecast_data['city']['coord']['lon'], 4)
                
                logger.info(f"Successfully fetched forecast for {city_name}, {country}")
                return render_template('forecast.html', forecast=forecast_list, city=city_name, country=country, 
                                     latitude=latitude, longitude=longitude, username=session.get('username'))
            except ValueError as e:
                logger.error(f"Validation error processing forecast data for {city}: {e}")
                error = "Error processing forecast data."
                return render_template('index.html', error=error, username=session.get('username'))
        else:
            logger.warning(f"City not found: {city}")
            error = f"City not found: {city}. Please enter a valid city name."
            return render_template('index.html', error=error, username=session.get('username'))
    
    except Exception as e:
        logger.error(f"Unexpected error in forecast route for city {request.args.get('city')}: {e}")
        error = f"An error occurred while fetching forecast data."
        return render_template('index.html', error=error, username=session.get('username'))


@app.route('/weather', methods=['GET', 'POST'])
def index():
    """Weather search page - requires login"""
    if 'user' not in session:
        logger.warning("Unauthenticated user attempting to access weather page")
        return redirect(url_for('login'))
    
    try:
        if request.method == 'POST':
            city = request.form.get('city', '').strip()
            
            if not city:
                logger.warning(f"Weather search from {session.get('user')} with empty city")
                error = "Please enter a city name!"
                return render_template('index.html', error=error, username=session.get('username'))
            
            logger.info(f"Fetching weather data for city: {city}")
            
            try:
                # Fetch current weather
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.Timeout:
                logger.error(f"Timeout error fetching weather for city: {city}")
                error = "Request timeout. Please try again."
                return render_template('index.html', error=error, username=session.get('username'))
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error fetching weather for city: {city} - {e}")
                error = "Could not fetch weather data from API."
                return render_template('index.html', error=error, username=session.get('username'))
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error fetching weather for city: {city} - {e}")
                error = "Network error occurred. Please check your connection."
                return render_template('index.html', error=error, username=session.get('username'))
            
            if data.get('cod') == 200:
                try:
                    weather = extract_weather_data(data)
                    weather['wind_direction'] = get_wind_direction(weather['wind_deg'])
                    
                    logger.debug(f"Successfully extracted weather data for {weather['city']}, {weather['country']}")
                    
                    # Fetch 5-day forecast
                    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
                    try:
                        forecast_response = requests.get(forecast_url, timeout=10)
                        forecast_response.raise_for_status()
                        forecast_data = forecast_response.json()
                        
                        if forecast_data.get('cod') == '200':
                            forecast = extract_forecast_data(forecast_data)
                            logger.info(f"Successfully fetched weather and forecast for {weather['city']}")
                        else:
                            logger.warning(f"Could not fetch forecast for {city}")
                            forecast = []
                    except requests.exceptions.Timeout:
                        logger.warning(f"Forecast request timeout for city: {city}, proceeding with empty forecast")
                        forecast = []
                    except requests.exceptions.RequestException as e:
                        logger.warning(f"Forecast request error for city: {city}, proceeding with empty forecast - {e}")
                        forecast = []
                    
                    return render_template('result.html', weather=weather, forecast=forecast, username=session.get('username'))
                
                except ValueError as e:
                    logger.error(f"Validation error processing weather data for {city}: {e}")
                    error = "Error processing weather data."
                    return render_template('index.html', error=error, username=session.get('username'))
            else:
                logger.warning(f"City not found: {city}")
                error = f"City not found: {city}. Please enter a valid city name."
                return render_template('index.html', error=error, username=session.get('username'))
        
        return render_template('index.html', username=session.get('username'))
    
    except Exception as e:
        logger.error(f"Unexpected error in weather route for city {request.form.get('city', 'unknown')}: {e}")
        error = "An error occurred while fetching weather data."
        return render_template('index.html', error=error, username=session.get('username'))

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    logger.error(f"400 Bad Request: {error}")
    return render_template('error.html', 
                         error_code=400, 
                         error_message="Bad Request - Invalid input provided"), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    logger.warning(f"404 Not Found: {request.url}")
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    logger.critical(f"500 Internal Server Error: {error}")
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal Server Error - Please try again later"), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all unhandled exceptions"""
    logger.critical(f"Unhandled exception: {error}", exc_info=True)
    return render_template('error.html', 
                         error_code=500, 
                         error_message="An unexpected error occurred"), 500


if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("Weather App Starting")
    logger.info("=" * 50)
    try:
        app.run(debug=True)
    except Exception as e:
        logger.critical(f"Critical error starting application: {e}")
        raise

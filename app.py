"""
Weather App - Main Application with Modular Architecture
Uses object-oriented design with Service Layer pattern
"""

from flask import Flask, render_template, request, redirect, url_for, session
from constant.header import API_KEY
from utils.app_logger import logger
from services import UserService, WeatherService
from datetime import datetime
import os

# ==================== App Initialization ====================

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Initialize services
user_service = UserService()
weather_service = WeatherService(API_KEY)

# ==================== Authentication Routes ====================

@app.route('/')
def home():
    """Redirect to login if not authenticated, else to weather page"""
    try:
        if 'user' in session:
            logger.info(f"User {session.get('user')} accessing home, redirecting to weather")
            return redirect(url_for('weather'))
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
                return render_template('login.html', error="Email and password are required!")
            
            logger.debug(f"Login attempt for email: {email}")
            
            # Authenticate user using UserService
            user = user_service.authenticate_user(email, password)
            
            if user:
                session['user'] = user.email
                session['username'] = user.username
                logger.info(f"Successful login for user: {email}")
                return redirect(url_for('weather'))
            else:
                logger.warning(f"Failed login attempt for email: {email}")
                return render_template('login.html', error="Invalid email or password!")
        
        return render_template('login.html')
    
    except Exception as e:
        logger.error(f"Unexpected error in login route: {e}")
        return render_template('login.html', error="An error occurred during login. Please try again.")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration"""
    try:
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validation
            if not all([username, email, password, confirm_password]):
                logger.warning("Signup attempt with missing fields")
                return render_template('signup.html', error="All fields are required!")
            
            if password != confirm_password:
                logger.warning(f"Signup attempt with mismatched passwords for email: {email}")
                return render_template('signup.html', error="Passwords do not match!")
            
            if len(password) < 6:
                logger.warning(f"Signup attempt with weak password for email: {email}")
                return render_template('signup.html', error="Password must be at least 6 characters!")
            
            # Register user using UserService
            if user_service.register_user(email, username, password):
                logger.info(f"New user registered successfully: {email}")
                success = "Account created successfully! Please login."
                return render_template('signup.html', success=success)
            else:
                logger.warning(f"Registration failed for email: {email}")
                error = "Email already registered or invalid data!"
                return render_template('signup.html', error=error)
        
        return render_template('signup.html')
    
    except Exception as e:
        logger.error(f"Unexpected error in signup route: {e}")
        return render_template('signup.html', error="An error occurred during signup. Please try again.")


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

# ==================== Weather Routes ====================

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    """Weather search page - requires authentication"""
    if 'user' not in session:
        logger.warning("Unauthenticated user attempting to access weather page")
        return redirect(url_for('login'))
    
    try:
        if request.method == 'POST':
            city = request.form.get('city', '').strip()
            
            if not city:
                logger.warning(f"Weather search from {session.get('user')} with empty city")
                return render_template('index.html', error="Please enter a city name!", 
                                     username=session.get('username'))
            
            logger.info(f"User {session.get('user')} searching weather for: {city}")
            
            # Fetch current weather using WeatherService
            weather_data = weather_service.get_current_weather(city)
            
            if not weather_data:
                logger.warning(f"City not found or API error: {city}")
                error = f"City '{city}' not found. Please check the spelling and try again."
                return render_template('index.html', error=error, 
                                     username=session.get('username'))
            
            # Fetch forecast
            forecast_list = weather_service.get_forecast(city)
            
            logger.info(f"Successfully fetched weather for {weather_data.city}, {weather_data.country}")
            
            # Render result even if forecast fails
            return render_template('result.html', 
                                 weather=weather_data.to_dict(),
                                 forecast=[f.to_dict() for f in forecast_list] if forecast_list else [],
                                 username=session.get('username'))
        
        return render_template('index.html', username=session.get('username'))
    
    except Exception as e:
        logger.error(f"Unexpected error in weather route: {e}", exc_info=True)
        return render_template('index.html', 
                             error=f"An error occurred: {str(e)}",
                             username=session.get('username'))


@app.route('/forecast', methods=['GET'])
def forecast():
    """Display 5-day forecast page - requires authentication"""
    if 'user' not in session:
        logger.warning("Unauthenticated user attempting to access forecast page")
        return redirect(url_for('login'))
    
    try:
        city = request.args.get('city', '').strip()
        
        if not city:
            logger.warning(f"Forecast request from {session.get('user')} without city parameter")
            return render_template('index.html', error="City not specified!", 
                                 username=session.get('username'))
        
        logger.info(f"User {session.get('user')} requesting forecast for: {city}")
        
        # Fetch forecast using WeatherService
        forecast_list = weather_service.get_forecast(city)
        
        if not forecast_list:
            logger.warning(f"City not found in forecast: {city}")
            error = f"City not found: {city}. Please enter a valid city name."
            return render_template('index.html', error=error, 
                                 username=session.get('username'))
        
        # Also fetch current weather to get coordinates
        weather_data = weather_service.get_current_weather(city)
        
        if weather_data:
            logger.info(f"Successfully fetched forecast for {weather_data.city}, {weather_data.country}")
            return render_template('forecast.html',
                                 forecast=[f.to_dict() for f in forecast_list],
                                 city=weather_data.city,
                                 country=weather_data.country,
                                 latitude=weather_data.latitude,
                                 longitude=weather_data.longitude,
                                 username=session.get('username'))
        else:
            return render_template('forecast.html',
                                 forecast=[f.to_dict() for f in forecast_list],
                                 city=city,
                                 country='',
                                 latitude=0,
                                 longitude=0,
                                 username=session.get('username'))
    
    except Exception as e:
        logger.error(f"Unexpected error in forecast route: {e}")
        error = "An error occurred while fetching forecast data."
        return render_template('index.html', error=error, 
                             username=session.get('username'))

# ==================== Error Handlers ====================

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


# ==================== App Startup ====================

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("Weather App Starting")
    logger.info("=" * 50)
    try:
        app.run(debug=True)
    except Exception as e:
        logger.critical(f"Critical error starting application: {e}")
        raise

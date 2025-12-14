# Quick Start Guide - Modular Architecture

## Files Overview

### 3 Core Modules

#### 1. `models.py` - Data Models (175 lines)
Defines type-safe data structures for the entire application.

```python
from models import User, WeatherData, ForecastDay, Session

# Create user
user = User(
    email="user@example.com",
    username="john_doe",
    password="secure_password"
)
user_dict = user.to_dict()

# Create weather data
weather = WeatherData(api_response)
weather_dict = weather.to_dict()

# Create forecast
forecast = ForecastDay(
    date="2025-12-15",
    day="Monday",
    forecast_data={...}
)
```

**When to use**:
- Need type-safe data representation
- Converting API responses to objects
- Passing data between layers
- Rendering in templates

---

#### 2. `services.py` - Business Logic (280+ lines)

Contains `UserService` and `WeatherService` for business operations.

```python
from services import UserService, WeatherService
from constant.header import API_KEY

# Initialize services
user_service = UserService()
weather_service = WeatherService(API_KEY)

# UserService methods
user = user_service.authenticate_user("user@example.com", "password")
success = user_service.register_user("new@example.com", "John", "password123")
exists = user_service.user_exists("user@example.com")

# WeatherService methods
weather = weather_service.get_current_weather("London")
forecast_list = weather_service.get_forecast("London")
```

**When to use**:
- Need to authenticate/register users
- Fetch weather data
- Process API responses
- Validate business logic
- Handle errors consistently

---

#### 3. `app.py` - Route Handlers (240 lines)

Flask application with clean route handlers that delegate to services.

```python
from flask import Flask, render_template, request, redirect, url_for, session
from services import UserService, WeatherService

app = Flask(__name__)
user_service = UserService()
weather_service = WeatherService(API_KEY)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    user = user_service.authenticate_user(email, password)
    if user:
        session['user'] = user.email
        return redirect(url_for('weather'))
    else:
        return render_template('login.html', error="Invalid credentials!")
```

**When to use**:
- Define HTTP routes
- Extract request data
- Call services
- Render templates
- Handle errors

---

## Common Tasks

### Add New Authentication Method

1. **Add to UserService** (services.py):
```python
class UserService:
    def verify_email(self, email: str) -> bool:
        """Verify if email is valid"""
        return '@' in email and '.' in email.split('@')[1]
```

2. **Use in Route** (app.py):
```python
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email', '').strip()
    if not user_service.verify_email(email):
        return render_template('signup.html', error="Invalid email!")
```

---

### Add New Weather Feature

1. **Add to WeatherData Model** (models.py):
```python
class WeatherData:
    def __init__(self, data: Dict):
        # ... existing fields ...
        self.uv_index = data.get('uvi', 0)  # New field
        self.air_quality = data.get('main', {})  # New field
```

2. **Update Service** (services.py):
```python
class WeatherService:
    def get_air_quality(self, city: str) -> Optional[Dict]:
        """Fetch air quality data"""
        url = "https://api.openweathermap.org/data/2.5/air_pollution"
        # Implementation
```

3. **Use in Route** (app.py):
```python
@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city', '').strip()
    weather_data = weather_service.get_current_weather(city)
    air_quality = weather_service.get_air_quality(city)
    return render_template('result.html', 
                         weather=weather_data.to_dict(),
                         air_quality=air_quality)
```

---

### Write Unit Tests

```python
import unittest
from services import UserService, WeatherService
from models import User, WeatherData

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.service = UserService()
    
    def test_register_user(self):
        result = self.service.register_user(
            'test@example.com',
            'testuser',
            'password123'
        )
        self.assertTrue(result)
    
    def test_authenticate_user(self):
        self.service.register_user('user@example.com', 'user', 'pass')
        user = self.service.authenticate_user('user@example.com', 'pass')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'user@example.com')

class TestWeatherData(unittest.TestCase):
    def test_weather_model(self):
        data = {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {'temp': 15.5, 'humidity': 75},
            'coord': {'lat': 51.5, 'lon': -0.1},
            'weather': [{'main': 'Cloudy', 'description': 'cloudy', 'icon': '04d'}],
            'wind': {'speed': 5.0, 'deg': 270}
        }
        weather = WeatherData(data)
        self.assertEqual(weather.city, 'London')
        self.assertEqual(weather.temperature, 15.5)

if __name__ == '__main__':
    unittest.main()
```

---

## Architecture Patterns Used

### 1. Service Layer Pattern
**Purpose**: Encapsulate business logic
```
Route → Service → Models/Database → Route
```

### 2. Data Model Pattern
**Purpose**: Type-safe data representation
```
API Response → Model → Validated Data → Template
```

### 3. Dependency Injection (Simple Form)
**Purpose**: Pass dependencies explicitly
```python
# Instead of: service = UserService()  # Inside function
# Do this: service = UserService()  # Initialize once, reuse
user_service = UserService()
weather_service = WeatherService(API_KEY)
```

### 4. Single Responsibility Principle (SRP)
**Purpose**: Each class has one reason to change
```
UserService - changes when user auth logic changes
WeatherService - changes when weather API changes
models.py - changes when data structure changes
app.py - changes when routing logic changes
```

---

## Performance Considerations

### Caching Example
```python
class CachedWeatherService(WeatherService):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.cache = {}
    
    def get_current_weather(self, city: str) -> Optional[WeatherData]:
        cache_key = city.lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        weather = super().get_current_weather(city)
        if weather:
            self.cache[cache_key] = weather
        return weather
```

### Database Migration Example
```python
class DatabaseUserService(UserService):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        db_user = self.db.query(User).filter_by(email=email).first()
        if db_user and db_user.password == password:
            return db_user
        return None
```

**No changes needed to routes!** This is the power of service layer pattern.

---

## Error Handling Strategy

### In Services (Catching Errors)
```python
class WeatherService:
    def get_current_weather(self, city: str) -> Optional[WeatherData]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return WeatherData(data)
        except requests.exceptions.Timeout:
            logger.error(f"Timeout for {city}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {city}: {e}")
            return None
```

### In Routes (Handling Errors)
```python
@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city', '').strip()
    
    weather_data = weather_service.get_current_weather(city)
    if not weather_data:
        return render_template('index.html', 
                             error=f"Failed to fetch weather for {city}")
    
    return render_template('result.html', weather=weather_data.to_dict())
```

---

## Logging Integration

```python
from utils.app_logger import logger

class UserService:
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        logger.debug(f"Authentication attempt for {email}")
        
        if email not in self.users:
            logger.warning(f"User not found: {email}")
            return None
        
        if self.users[email]['password'] == password:
            logger.info(f"Successful authentication: {email}")
            return User.from_dict(email, self.users[email])
        else:
            logger.warning(f"Failed authentication: {email}")
            return None
```

All logs automatically go to:
- `logs/weather_app_*.log` (file)
- Console output (for development)

---

## Deployment Checklist

- [ ] Update API key in `constant/header.py`
- [ ] Change secret key in `app.py`
- [ ] Use production WSGI server (not Flask dev server)
- [ ] Set `debug=False` in `app.py`
- [ ] Use database instead of JSON for users
- [ ] Hash passwords with bcrypt
- [ ] Add HTTPS/SSL certificate
- [ ] Set up error monitoring
- [ ] Configure log rotation

---

## Key Takeaways

1. **models.py** = Pure data structures
2. **services.py** = Business logic & APIs
3. **app.py** = HTTP handling only

✅ Each module can be tested independently
✅ Easy to replace or extend any layer
✅ Services are reusable across multiple routes
✅ Models are type-safe and validated
✅ Clear data flow through the application

The architecture is **production-ready** and **scalable**!

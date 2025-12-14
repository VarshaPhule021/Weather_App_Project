# Class Diagram - Weather App (Modular Architecture)

## Overview
The class diagram shows the refactored modular architecture with separate models, services, and route handlers.

---

## Complete Class Hierarchy

```
┌─────────────────────────────────────────────────────────────────────┐
│                   MODELS LAYER (models.py)                          │
│                  Type-Safe Data Structures                           │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐  ┌──────────────────────────────┐
│         User                 │  │      WeatherData             │
├──────────────────────────────┤  ├──────────────────────────────┤
│ - email: str                 │  │ - city: str                  │
│ - username: str              │  │ - country: str               │
│ - password: str              │  │ - temperature: float         │
│ - created_at: str            │  │ - feels_like: float          │
├──────────────────────────────┤  │ - temp_min: float            │
│ + to_dict(): Dict            │  │ - temp_max: float            │
│ + from_dict(): User          │  │ - humidity: int              │
└──────────────────────────────┘  │ - pressure: int              │
                                   │ - visibility: float          │
                                   │ - wind_speed: float          │
                                   │ - wind_deg: int              │
                                   │ - wind_gust: float           │
                                   │ - cloudiness: int            │
                                   │ - main_condition: str        │
                                   │ - description: str           │
                                   │ - icon: str                  │
                                   │ - sunrise: str               │
                                   │ - sunset: str                │
                                   │ - rain: float                │
                                   │ - snow: float                │
                                   │ - latitude: float            │
                                   │ - longitude: float           │
                                   │ - wind_direction: str        │
                                   │ - timezone: int              │
                                   ├──────────────────────────────┤
                                   │ + to_dict(): Dict            │
                                   │ + __repr__(): str            │
                                   └──────────────────────────────┘

┌──────────────────────────────┐  ┌──────────────────────────────┐
│      ForecastDay             │  │      Session                 │
├──────────────────────────────┤  ├──────────────────────────────┤
│ - date: str                  │  │ - user_email: str            │
│ - day: str                   │  │ - username: str              │
│ - temp_max: float            │  │ - created_at: datetime       │
│ - temp_min: float            │  │ - last_activity: datetime    │
│ - temp: float                │  ├──────────────────────────────┤
│ - humidity: int              │  │ + update_activity(): None    │
│ - description: str           │  │ + __repr__(): str            │
│ - icon: str                  │  └──────────────────────────────┘
│ - wind_speed: float          │
│ - rain_chance: float         │
├──────────────────────────────┤
│ + to_dict(): Dict            │
│ + __repr__(): str            │
└──────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                  SERVICES LAYER (services.py)                       │
│               Business Logic & External Integration                 │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│      UserService                 │  │    WeatherService                │
├──────────────────────────────────┤  ├──────────────────────────────────┤
│ - USERS_FILE: str = 'users.json' │  │ - CURRENT_WEATHER_URL: str       │
│ - users: Dict                    │  │ - FORECAST_URL: str              │
├──────────────────────────────────┤  │ - REQUEST_TIMEOUT: int = 10      │
│ + __init__()                     │  │ - api_key: str                   │
│ + _load_users() → Dict           │  ├──────────────────────────────────┤
│ + _save_users() → None           │  │ + __init__(api_key: str)         │
│ + register_user(email, username, │  │ + get_current_weather(city) →    │
│   password) → bool               │  │   Optional[WeatherData]          │
│ + authenticate_user(email,       │  │ + get_forecast(city) →           │
│   password) → Optional[User]     │  │   Optional[List[ForecastDay]]    │
│ + user_exists(email) → bool      │  │ + _get_wind_direction(degrees) → │
│ + get_user(email) →              │  │   str                            │
│   Optional[User]                 │  └──────────────────────────────────┘
└──────────────────────────────────┘
        ▲                                      ▲
        │ creates/returns                      │ creates/returns
        │                                      │
        │                                      ▼
        │                            ┌──────────────────────────┐
        │                            │    WeatherData           │
        │                            │    ForecastDay[]         │
        │                            └──────────────────────────┘
        │
        ▼
    ┌──────────────────────────┐
    │    User                  │
    │    WeatherData[]         │
    └──────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    ROUTES LAYER (app.py)                            │
│               HTTP Handlers - Clean & Simple                        │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│              Flask Application                                   │
├──────────────────────────────────────────────────────────────────┤
│ - app: Flask                                                     │
│ - user_service: UserService                                     │
│ - weather_service: WeatherService                               │
├──────────────────────────────────────────────────────────────────┤
│ AUTHENTICATION ROUTES:                                          │
│ + home() → redirect based on session                            │
│ + login() → POST calls user_service.authenticate_user()        │
│ + signup() → POST calls user_service.register_user()          │
│ + logout() → clear session                                      │
│                                                                  │
│ WEATHER ROUTES:                                                 │
│ + weather() → POST calls weather_service.get_current_weather() │
│ + forecast() → GET calls weather_service.get_forecast()       │
│                                                                  │
│ ERROR HANDLERS:                                                 │
│ + @errorhandler(400) → bad_request()                           │
│ + @errorhandler(404) → not_found()                             │
│ + @errorhandler(500) → internal_error()                        │
│ + @errorhandler(Exception) → handle_exception()               │
└──────────────────────────────────────────────────────────────────┘
       │
       │ initializes & uses
       │
       ├──→ user_service: UserService
       │
       └──→ weather_service: WeatherService
```

---

## Detailed Class Diagrams by Module

### Module: models.py

#### User Class
```
┌─────────────────────────────────────────────────┐
│              User                               │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│  - email: str                (user email)       │
│  - username: str             (display name)     │
│  - password: str             (password)         │
│  - created_at: str           (timestamp)        │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│  + __init__(email, username, password,         │
│             created_at=None)                    │
│  + to_dict() → Dict                             │
│      Returns: {'username': ..., 'password': ...│
│  + from_dict(email: str, data: Dict)           │
│      Class method: creates User from dict      │
│  + __repr__() → str                             │
├─────────────────────────────────────────────────┤
│ Purpose:                                        │
│  Type-safe user data representation            │
│  Immutable or semi-immutable                   │
└─────────────────────────────────────────────────┘
```

#### WeatherData Class
```
┌─────────────────────────────────────────────────┐
│           WeatherData                           │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│  - city: str                 (city name)        │
│  - country: str              (country code)     │
│  - temperature: float        (current temp)     │
│  - humidity: int             (humidity %)       │
│  - wind_speed: float         (wind speed)       │
│  - wind_direction: str       (N, NE, E, ...)   │
│  - ... (15+ more attributes)                   │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│  + __init__(data: Dict)                         │
│      Initializes from API response              │
│  + to_dict() → Dict                             │
│      Returns all attributes as dictionary       │
│  + __repr__() → str                             │
├─────────────────────────────────────────────────┤
│ Purpose:                                        │
│  Type-safe weather data container              │
│  Validates and normalizes API response         │
└─────────────────────────────────────────────────┘
```

#### ForecastDay Class
```
┌─────────────────────────────────────────────────┐
│           ForecastDay                           │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│  - date: str                 (YYYY-MM-DD)       │
│  - day: str                  (Monday, etc.)     │
│  - temp_max: float           (max temperature)  │
│  - temp_min: float           (min temperature)  │
│  - humidity: int             (humidity %)       │
│  - rain_chance: float        (rain %)           │
│  - wind_speed: float                            │
│  - description: str          (weather desc)     │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│  + __init__(date, day, forecast_data)         │
│  + to_dict() → Dict                             │
│  + __repr__() → str                             │
├─────────────────────────────────────────────────┤
│ Purpose:                                        │
│  Represents one day's forecast                  │
│  Part of 5-day forecast list                    │
└─────────────────────────────────────────────────┘
```

#### Session Class
```
┌─────────────────────────────────────────────────┐
│            Session                              │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│  - user_email: str           (user's email)     │
│  - username: str             (user's name)      │
│  - created_at: datetime      (creation time)    │
│  - last_activity: datetime   (last activity)    │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│  + __init__(user_email, username)              │
│  + update_activity() → None                     │
│      Updates last_activity timestamp            │
│  + __repr__() → str                             │
├─────────────────────────────────────────────────┤
│ Purpose:                                        │
│  Represents active user session                 │
│  Tracks session activity                        │
└─────────────────────────────────────────────────┘
```

### Module: services.py

#### UserService Class
```
┌─────────────────────────────────────────────────┐
│          UserService                            │
├─────────────────────────────────────────────────┤
│ Class Attributes:                               │
│  - USERS_FILE: str = 'users.json'              │
├─────────────────────────────────────────────────┤
│ Instance Attributes:                            │
│  - users: Dict[str, Dict]                       │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│  + __init__()                                   │
│      Initializes and loads users                │
│                                                 │
│  + _load_users() → Dict[str, Dict]             │
│      Loads from users.json file                 │
│      Returns: {email: user_data}                │
│                                                 │
│  + _save_users() → None                         │
│      Saves users to users.json file             │
│      Raises: IOError, json.JSONEncodeError     │
│                                                 │
│  + register_user(email: str, username: str,    │
│                  password: str) → bool          │
│      Validates and registers new user           │
│      Returns: True if success, False if error   │
│      Validates: unique email, password length   │
│                                                 │
│  + authenticate_user(email: str,                │
│                      password: str)             │
│      → Optional[User]                           │
│      Authenticates user credentials             │
│      Returns: User object if valid, None else   │
│                                                 │
│  + user_exists(email: str) → bool              │
│      Checks if user exists                      │
│                                                 │
│  + get_user(email: str) → Optional[User]       │
│      Retrieves user by email                    │
├─────────────────────────────────────────────────┤
│ Error Handling:                                 │
│  - File I/O errors                              │
│  - JSON decode/encode errors                    │
│  - Validation failures                          │
│  - All logged comprehensively                   │
├─────────────────────────────────────────────────┤
│ Purpose:                                        │
│  Centralize user management logic              │
│  Handle authentication & registration          │
│  Persist user data to storage                  │
└─────────────────────────────────────────────────┘
```

#### WeatherService Class
```
┌──────────────────────────────────────────────────┐
│         WeatherService                           │
├──────────────────────────────────────────────────┤
│ Class Attributes:                                │
│  - CURRENT_WEATHER_URL: str                      │
│    = "https://api.openweathermap.org/.../weather│
│  - FORECAST_URL: str                             │
│    = "https://api.openweathermap.org/.../forecast
│  - REQUEST_TIMEOUT: int = 10 (seconds)          │
├──────────────────────────────────────────────────┤
│ Instance Attributes:                             │
│  - api_key: str                                  │
├──────────────────────────────────────────────────┤
│ Methods:                                         │
│  + __init__(api_key: str)                        │
│      Initializes with OpenWeather API key        │
│                                                  │
│  + get_current_weather(city: str)               │
│      → Optional[WeatherData]                     │
│      Fetches current weather from API            │
│      - Makes HTTP request with 10s timeout       │
│      - Validates response                        │
│      - Creates WeatherData object                │
│      - Sets wind_direction from degrees         │
│      Returns: WeatherData if success, None else │
│                                                  │
│  + get_forecast(city: str)                      │
│      → Optional[List[ForecastDay]]              │
│      Fetches 5-day forecast from API             │
│      - Makes HTTP request                        │
│      - Processes forecast data                   │
│      - Creates ForecastDay objects               │
│      - Returns only first 5 days                 │
│      Returns: List of ForecastDay if success    │
│                                                  │
│  + _get_wind_direction(degrees: float) → str    │
│      Converts wind degrees to compass direction │
│      Input: 0-360 degrees                        │
│      Output: 'N', 'NE', 'E', ..., 'NNW'        │
├──────────────────────────────────────────────────┤
│ Error Handling:                                  │
│  - Timeout errors (requests.exceptions.Timeout) │
│  - HTTP errors (raise_for_status)               │
│  - Network errors (RequestException)             │
│  - Missing data validation                       │
│  - Returns None on any error                     │
│  - Comprehensive logging                        │
├──────────────────────────────────────────────────┤
│ Purpose:                                         │
│  Handle all weather API interactions             │
│  Transform API responses to typed models         │
│  Provide clean interface to routes               │
└──────────────────────────────────────────────────┘
```

### Module: app.py (Route Handlers)

#### Route Functions
```
┌────────────────────────────────────────────────┐
│         Authentication Routes                  │
├────────────────────────────────────────────────┤
│ home() [GET /]                                 │
│  ├─ Checks if 'user' in session                │
│  ├─ If yes → redirect('/weather')             │
│  └─ If no → redirect('/login')                │
│                                                │
│ login() [GET/POST /login]                      │
│  ├─ GET: Render login template                 │
│  └─ POST: Extract email/password               │
│     → user_service.authenticate_user()         │
│     → Set session if success                   │
│     → Return error if failed                   │
│                                                │
│ signup() [GET/POST /signup]                    │
│  ├─ GET: Render signup template                │
│  └─ POST: Validate & extract form data        │
│     → user_service.register_user()             │
│     → Return success or error page             │
│                                                │
│ logout() [GET /logout]                         │
│  ├─ Clear session                              │
│  └─ Redirect to login                          │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│          Weather Routes                        │
├────────────────────────────────────────────────┤
│ weather() [GET/POST /weather]                  │
│  ├─ Check authentication (session['user'])    │
│  ├─ GET: Render weather search page            │
│  └─ POST: Extract city from form              │
│     → weather_service.get_current_weather()    │
│     → weather_service.get_forecast()           │
│     → Render result template with data         │
│                                                │
│ forecast() [GET /forecast]                     │
│  ├─ Check authentication                       │
│  ├─ Extract city from query param              │
│  ├─ weather_service.get_forecast(city)        │
│  └─ Render forecast template                   │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│         Error Handlers                         │
├────────────────────────────────────────────────┤
│ bad_request() [@errorhandler(400)]            │
│  → Render error.html with 400 code             │
│                                                │
│ not_found() [@errorhandler(404)]              │
│  → Render error.html with 404 code             │
│                                                │
│ internal_error() [@errorhandler(500)]         │
│  → Render error.html with 500 code             │
│                                                │
│ handle_exception() [@errorhandler(Exception)]  │
│  → Render error.html with generic message      │
└────────────────────────────────────────────────┘
```
```

---

## Relationships

### Inheritance
```
None (Flask application doesn't use inheritance)
```

### Composition
```
Flask Application
  ├─ contains → User Service
  ├─ contains → Weather Service
  ├─ contains → Logger Service
  ├─ contains → Session Manager
  └─ contains → Exception Handler
```

### Association
```
User Service ──→ User Model (1 to Many)
Weather Service ──→ Weather Model (1 to 1)
Weather Service ──→ Forecast Model (1 to Many)
Logger Service ──→ Handler Service (1 to Many)
```

### Dependency
```
Flask Application ──depends on→ requests (HTTP library)
Flask Application ──depends on→ json (JSON parser)
Weather Service ──depends on→ requests
Logger Service ──depends on→ logging (Python stdlib)
```

---

## Detailed Class Descriptions

### 1. **Flask Application**
```
Class: WeatherApp
Type: Main Application Class

Responsibilities:
- Route handling
- Request processing
- Response rendering
- Error handling

Key Methods:
- home() → Redirect to login/weather
- login() → Authenticate user
- signup() → Register new user
- logout() → Clear session
- index() → Weather search page
- forecast() → Forecast page
```

### 2. **User Model**
```
Class: User
Type: Domain Model

Attributes:
- email: str (unique, primary key)
- username: str
- password: str (hashed)
- created_at: datetime

Methods:
- validate_email() → Check email format
- validate_password() → Check password strength
- to_dict() → Convert to dictionary
```

### 3. **Weather Model**
```
Class: Weather
Type: Domain Model

Attributes:
- city: str
- country: str
- coordinates: (latitude, longitude)
- temperature: float
- wind: (speed, direction, gust)
- humidity: int
- pressure: int
- visibility: float
- clouds: int
- precipitation: (rain, snow)
- sun_times: (sunrise, sunset)

Methods:
- get_icon_url() → Get weather icon
- get_wind_direction() → Convert degrees to direction
- to_dict() → Convert to dictionary
```

### 4. **Forecast Model**
```
Class: Forecast
Type: Domain Model

Attributes:
- date: str (YYYY-MM-DD)
- day: str (Monday, Tuesday, etc.)
- temp: (min, max, current)
- humidity: int
- description: str
- icon: str
- wind_speed: float
- rain_chance: float

Methods:
- to_dict() → Convert to dictionary
- get_icon_url() → Get forecast icon
```

### 5. **User Service**
```
Class: UserService
Type: Service Layer

Responsibilities:
- User authentication
- User registration
- User data persistence
- Data validation

Methods:
- load_users() → Load from JSON
- save_users() → Save to JSON
- authenticate(email, password) → Verify credentials
- register(user) → Create new user
- user_exists(email) → Check existence
```

### 6. **Weather Service**
```
Class: WeatherService
Type: Service Layer

Responsibilities:
- API communication
- Data extraction
- Data transformation
- Error handling

Methods:
- fetch_weather(city) → Get current weather
- fetch_forecast(city) → Get 5-day forecast
- extract_weather_data(response) → Parse weather
- extract_forecast_data(response) → Parse forecast
- get_wind_direction(degrees) → Convert wind direction
```

### 7. **Logger Service**
```
Class: AppLogger
Type: Utility Service

Responsibilities:
- Centralized logging
- Log configuration
- Log rotation
- Handler management

Methods:
- get_logger() → Return logger instance
- add_file_handler() → Add file output
- add_console_handler() → Add console output
- setup_rotation() → Configure rotation
```

### 8. **Session Manager**
```
Class: SessionManager
Type: Service Layer

Responsibilities:
- Session creation
- Session validation
- Session destruction
- Session data management

Methods:
- create_session(user) → Start session
- get_session(user_id) → Retrieve session
- destroy_session(user_id) → End session
- validate_session() → Check validity
```

### 9. **Exception Handler**
```
Class: ExceptionHandler
Type: Error Handling

Responsibilities:
- Error catching
- Error logging
- Error response generation
- User notification

Methods:
- handle_400() → Bad request
- handle_404() → Not found
- handle_500() → Server error
- handle_generic() → Any exception
```

---

## Method Signatures

### User Service
```python
def load_users() -> Dict[str, User]
def save_users(users: Dict[str, User]) -> None
def authenticate(email: str, password: str) -> bool
def register(username: str, email: str, password: str) -> bool
```

### Weather Service
```python
def fetch_weather(city: str) -> Dict
def fetch_forecast(city: str) -> Dict
def extract_weather_data(data: Dict) -> Weather
def extract_forecast_data(data: Dict) -> List[Forecast]
def get_wind_direction(degrees: int) -> str
```

### Logger Service
```python
def get_logger() -> logging.Logger
def log_info(message: str) -> None
def log_error(message: str, exc_info: bool = False) -> None
def log_warning(message: str) -> None
def log_debug(message: str) -> None
```

---

## Design Patterns Used

1. **MVC Pattern**
   - Model: User, Weather, Forecast
   - View: HTML templates
   - Controller: Flask routes

2. **Service Layer Pattern**
   - UserService, WeatherService, LoggerService
   - Separation of concerns

3. **Singleton Pattern**
   - Logger instance (single throughout app)
   - Database connection (users.json)

4. **Factory Pattern**
   - User creation from registration
   - Session creation from authentication

5. **Strategy Pattern**
   - Multiple exception handlers
   - Different log handlers (file, console)

---

## Encapsulation

### Private Attributes (Protected)
```
- _api_key (API configuration)
- _log_dir (Logger configuration)
- _session_data (Session information)
```

### Public Methods
```
- login(), logout(), signup()
- search_weather(), view_forecast()
- get_logger(), log_error()
```

### Properties
```
@property
def current_user() -> User:
    return session.get('user')

@property
def is_authenticated() -> bool:
    return 'user' in session
```

---

## Class Interactions

```
User Request
    │
    ▼
Flask Route Handler
    │
    ├─→ Session Manager (validate session)
    │
    ├─→ User Service (authenticate)
    │
    ├─→ Weather Service (fetch data)
    │
    ├─→ Logger Service (log event)
    │
    └─→ Exception Handler (catch errors)
         │
         ▼
    Response/Template
```

---

## Summary

| Class | Type | Purpose |
|-------|------|---------|
| WeatherApp | Main | Application entry point |
| User | Model | User data structure |
| Weather | Model | Weather data structure |
| Forecast | Model | Forecast data structure |
| UserService | Service | User management |
| WeatherService | Service | Weather data |
| LoggerService | Service | Logging |
| SessionManager | Service | Session handling |
| ExceptionHandler | Utility | Error handling |

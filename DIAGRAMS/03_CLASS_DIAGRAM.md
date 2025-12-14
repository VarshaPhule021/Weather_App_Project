# Class Diagram - Weather App

## Overview
The class diagram shows the structure of the Weather App with classes, attributes, methods, and relationships.

---

## Class Diagram (ASCII)

```
┌────────────────────────────────────┐
│          Flask Application         │
├────────────────────────────────────┤
│ - app: Flask                       │
│ - secret_key: str                  │
│ - API_KEY: str                     │
├────────────────────────────────────┤
│ + home()                           │
│ + login()                          │
│ + signup()                         │
│ + logout()                         │
│ + index()                          │
│ + forecast()                       │
│ + errorhandler()                   │
└────────────────────────────────────┘
           │
           │ uses
           ▼
┌────────────────────────────────────┐
│        User Service                │
├────────────────────────────────────┤
│ - users_file: str                  │
├────────────────────────────────────┤
│ + load_users(): dict               │
│ + save_users(users: dict): void    │
└────────────────────────────────────┘
           │
           │ manages
           ▼
┌────────────────────────────────────┐
│          User Model                │
├────────────────────────────────────┤
│ - email: str                       │
│ - username: str                    │
│ - password: str                    │
│ - created_at: datetime             │
├────────────────────────────────────┤
│ + validate_email(): bool           │
│ + validate_password(): bool        │
│ + to_dict(): dict                  │
└────────────────────────────────────┘


┌────────────────────────────────────┐
│       Weather Service              │
├────────────────────────────────────┤
│ - api_key: str                     │
│ - base_url: str                    │
│ - timeout: int                     │
├────────────────────────────────────┤
│ + fetch_weather(city): dict        │
│ + fetch_forecast(city): dict       │
│ + extract_weather_data(data): dict │
│ + extract_forecast_data(data): list│
│ + get_wind_direction(deg): str     │
└────────────────────────────────────┘
           │
           │ returns
           ▼
┌────────────────────────────────────┐
│       Weather Model                │
├────────────────────────────────────┤
│ - city: str                        │
│ - country: str                     │
│ - temperature: float               │
│ - feels_like: float                │
│ - temp_min: float                  │
│ - temp_max: float                  │
│ - humidity: int                    │
│ - pressure: int                    │
│ - visibility: float                │
│ - wind_speed: float                │
│ - wind_deg: int                    │
│ - wind_gust: float                 │
│ - cloudiness: int                  │
│ - main_condition: str              │
│ - description: str                 │
│ - icon: str                        │
│ - sunrise: str                     │
│ - sunset: str                      │
│ - rain: float                      │
│ - snow: float                      │
│ - latitude: float                  │
│ - longitude: float                 │
├────────────────────────────────────┤
│ + to_dict(): dict                  │
│ + get_icon_url(): str              │
│ + get_wind_direction(): str        │
└────────────────────────────────────┘


┌────────────────────────────────────┐
│       Forecast Model               │
├────────────────────────────────────┤
│ - date: str                        │
│ - day: str                         │
│ - temp_max: float                  │
│ - temp_min: float                  │
│ - temp: float                      │
│ - humidity: int                    │
│ - description: str                 │
│ - icon: str                        │
│ - wind_speed: float                │
│ - rain_chance: float               │
├────────────────────────────────────┤
│ + to_dict(): dict                  │
│ + get_icon_url(): str              │
└────────────────────────────────────┘


┌────────────────────────────────────┐
│       Logger Service               │
├────────────────────────────────────┤
│ - logger: Logger                   │
│ - log_dir: str                     │
├────────────────────────────────────┤
│ + get_logger(): Logger             │
│ + log_info(msg): void              │
│ + log_error(msg): void             │
│ + log_warning(msg): void           │
│ + log_debug(msg): void             │
└────────────────────────────────────┘
           │
           │ configures
           ▼
┌────────────────────────────────────┐
│       Handler Service              │
├────────────────────────────────────┤
│ - handlers: list                   │
├────────────────────────────────────┤
│ + add_file_handler(): void         │
│ + add_console_handler(): void      │
│ + setup_rotation(): void           │
└────────────────────────────────────┘


┌────────────────────────────────────┐
│     Exception Handler              │
├────────────────────────────────────┤
│ - error_code: int                  │
│ - error_message: str               │
│ - timestamp: datetime              │
├────────────────────────────────────┤
│ + handle_400(): Response           │
│ + handle_404(): Response           │
│ + handle_500(): Response           │
│ + handle_generic(): Response       │
└────────────────────────────────────┘


┌────────────────────────────────────┐
│      Session Manager               │
├────────────────────────────────────┤
│ - session_data: dict               │
├────────────────────────────────────┤
│ + create_session(user): void       │
│ + get_session(user_id): dict       │
│ + destroy_session(user_id): void   │
│ + validate_session(): bool         │
└────────────────────────────────────┘
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

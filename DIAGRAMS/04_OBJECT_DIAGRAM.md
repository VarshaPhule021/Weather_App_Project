# Object Diagram - Weather App (Modular Architecture)

## Overview
The object diagram shows instances of classes and their relationships during runtime execution using the new modular architecture with UserService, WeatherService, and data models.

---

## Object Diagram: User Registration & Login

```
Scenario: User "john@example.com" logged in

┌──────────────────────────────────┐
│  john_user: User                 │
├──────────────────────────────────┤
│ email = "john@example.com"       │
│ username = "john_doe"            │
│ password = "hashed_pwd_123"      │
│ created_at = "2025-12-14 10:30"  │
└──────────────────────────────────┘
         │
         │ has_session
         ▼
┌──────────────────────────────────┐
│  john_session: Session           │
├──────────────────────────────────┤
│ user_id = "john@example.com"     │
│ username = "john_doe"            │
│ created_at = "2025-12-14 10:35"  │
│ timeout = 3600                   │
└──────────────────────────────────┘
         │
         │ interacts_with
         ▼
┌──────────────────────────────────┐
│  flask_app: Flask                │
├──────────────────────────────────┤
│ secret_key = "secret_123"        │
│ debug = True                     │
│ host = "127.0.0.1"               │
│ port = 5000                      │
└──────────────────────────────────┘
```

---

## Object Diagram 2: Weather Search Instance

```
Scenario: User searches for "London"

┌──────────────────────────────────┐
│  london_weather: Weather         │
├──────────────────────────────────┤
│ city = "London"                  │
│ country = "GB"                   │
│ temperature = 12.5               │
│ feels_like = 10.2                │
│ temp_min = 8.3                   │
│ temp_max = 15.1                  │
│ humidity = 75                    │
│ pressure = 1013                  │
│ visibility = 10.0                │
│ wind_speed = 3.5                 │
│ wind_deg = 270                   │
│ wind_direction = "W"             │
│ wind_gust = 5.2                  │
│ cloudiness = 60                  │
│ main_condition = "Cloudy"        │
│ description = "Overcast Clouds"  │
│ icon = "04d"                     │
│ sunrise = "7:30 AM"              │
│ sunset = "4:15 PM"               │
│ rain = 0.0                       │
│ snow = 0.0                       │
│ latitude = 51.5074               │
│ longitude = -0.1278              │
└──────────────────────────────────┘
         │
         │ has_forecast
         ▼
┌─────────────────────────┐    ┌─────────────────────────┐
│ day1_forecast:Forecast  │    │ day2_forecast:Forecast  │
├─────────────────────────┤    ├─────────────────────────┤
│ date = "2025-12-15"     │    │ date = "2025-12-16"     │
│ day = "Monday"          │    │ day = "Tuesday"         │
│ temp_max = 16.5         │    │ temp_max = 14.2         │
│ temp_min = 9.1          │    │ temp_min = 7.8          │
│ description = "Partly   │    │ description = "Rainy"   │
│  Cloudy"                │    │ rain_chance = 85.0      │
│ rain_chance = 20.0      │    │ wind_speed = 4.2        │
│ wind_speed = 2.8        │    └─────────────────────────┘
│ humidity = 70           │
└─────────────────────────┘
         │
         │ other_days...
         ▼
    [day3, day4, day5 objects...]
         │
         │ visualized_on
         ▼
┌──────────────────────────────────┐
│  leaflet_map: LeafletMap         │
├──────────────────────────────────┤
│ latitude = 51.5074               │
│ longitude = -0.1278              │
│ zoom_level = 11                  │
│ tile_layer = "openstreetmap"     │
│ marker_popup = "London, GB"      │
└──────────────────────────────────┘
```

---

## Object Diagram 3: API Response Instance

```
Scenario: Weather API call returns response

┌────────────────────────────────────┐
│  api_request: HTTPRequest          │
├────────────────────────────────────┤
│ method = "GET"                     │
│ url = "api.openweathermap.org/..." │
│ params.q = "London"                │
│ params.appid = "API_KEY_123"       │
│ params.units = "metric"            │
│ timeout = 10                       │
└────────────────────────────────────┘
         │
         │ returns
         ▼
┌────────────────────────────────────┐
│  api_response: HTTPResponse        │
├────────────────────────────────────┤
│ status_code = 200                  │
│ content_type = "application/json"  │
│ body = {JSON weather data}         │
│ headers.server = "nginx"           │
│ headers.date = "2025-12-14..."     │
│ elapsed_time = 0.342               │
└────────────────────────────────────┘
         │
         │ parsed_to
         ▼
┌────────────────────────────────────┐
│  response_data: Dict               │
├────────────────────────────────────┤
│ cod = "200"                        │
│ name = "London"                    │
│ sys.country = "GB"                 │
│ sys.sunrise = 1702546400           │
│ sys.sunset = 1702574100            │
│ coord.lat = 51.5074                │
│ coord.lon = -0.1278                │
│ main.temp = 12.5                   │
│ main.feels_like = 10.2             │
│ main.temp_min = 8.3                │
│ main.temp_max = 15.1               │
│ main.humidity = 75                 │
│ main.pressure = 1013               │
│ wind.speed = 3.5                   │
│ wind.deg = 270                     │
│ clouds.all = 60                    │
│ weather[0].main = "Clouds"         │
│ weather[0].description = "..."     │
└────────────────────────────────────┘
         │
         │ logged_as
         ▼
┌────────────────────────────────────┐
│  log_entry: LogRecord              │
├────────────────────────────────────┤
│ timestamp = "2025-12-14 15:45:30"  │
│ logger = "WeatherApp"              │
│ level = "INFO"                     │
│ message = "Successfully fetched..."│
│ filename = "app.py"                │
│ lineno = 234                       │
└────────────────────────────────────┘
```

---

## Object Diagram 4: Error Handling Instance

```
Scenario: User enters invalid city name

┌──────────────────────────────────┐
│  user_input: str                 │
├──────────────────────────────────┤
│ value = "XyZ$#"                  │
└──────────────────────────────────┘
         │
         │ triggers
         ▼
┌──────────────────────────────────┐
│  validation_error: ValueError    │
├──────────────────────────────────┤
│ message = "Invalid city format"  │
│ traceback = [stack trace]        │
└──────────────────────────────────┘
         │
         │ caught_by
         ▼
┌──────────────────────────────────┐
│  exception_handler: Handler      │
├──────────────────────────────────┤
│ error_code = 400                 │
│ error_type = "ValueError"        │
│ timestamp = "2025-12-14 15:46"   │
└──────────────────────────────────┘
         │
         │ logs_to
         ▼
┌──────────────────────────────────┐
│  error_log: LogRecord            │
├──────────────────────────────────┤
│ level = "WARNING"                │
│ message = "Invalid input: ..."   │
│ exception = ValueError           │
│ stacktrace = [details]           │
└──────────────────────────────────┘
         │
         │ returns
         ▼
┌──────────────────────────────────┐
│  error_response: Response        │
├──────────────────────────────────┤
│ status_code = 400                │
│ content_type = "text/html"       │
│ template = "error.html"          │
│ context.error_code = 400         │
│ context.message = "Invalid input"│
│ context.suggestion = "..."       │
└──────────────────────────────────┘
         │
         │ displayed_as
         ▼
┌──────────────────────────────────┐
│  error_page: HTML                │
├──────────────────────────────────┤
│ title = "Error 400"              │
│ heading = "Bad Request"          │
│ message = "Invalid input"        │
│ buttons = ["Home", "Back"]       │
└──────────────────────────────────┘
```

---

## Object Diagram 5: Authentication Flow Instance

```
Scenario: User authentication process

┌─────────────────────────────────┐
│  signup_form: Form              │
├─────────────────────────────────┤
│ username = "jane_doe"           │
│ email = "jane@example.com"      │
│ password = "SecurePass123"      │
│ confirm_password = "SecurePass123"
└─────────────────────────────────┘
         │
         │ validates
         ▼
┌─────────────────────────────────┐
│  validation_result: bool        │
├─────────────────────────────────┤
│ is_valid = True                 │
│ empty_check = True              │
│ password_match = True           │
│ password_length = True          │
│ email_unique = True             │
└─────────────────────────────────┘
         │
         │ creates
         ▼
┌─────────────────────────────────┐
│  new_user: User                 │
├─────────────────────────────────┤
│ email = "jane@example.com"      │
│ username = "jane_doe"           │
│ password = "hashed_pwd_456"     │
│ created_at = "2025-12-14 16:00" │
└─────────────────────────────────┘
         │
         │ persists_to
         ▼
┌─────────────────────────────────┐
│  users_file: JSON               │
├─────────────────────────────────┤
│ format = ".json"                │
│ location = "users.json"         │
│ permissions = "read/write"      │
│ encoding = "utf-8"              │
└─────────────────────────────────┘
         │
         │ logged_as
         ▼
┌─────────────────────────────────┐
│  audit_log: LogRecord           │
├─────────────────────────────────┤
│ level = "INFO"                  │
│ event = "user_signup"           │
│ user_email = "jane@example.com" │
│ timestamp = "2025-12-14 16:00"  │
│ ip_address = "192.168.1.100"    │
└─────────────────────────────────┘
```

---

## Object Diagram 6: Logging System Instance

```
Scenario: Logger configuration and usage

┌────────────────────────────────────┐
│  logger: Logger                    │
├────────────────────────────────────┤
│ name = "WeatherApp"                │
│ level = DEBUG                      │
│ handlers = [file_h, console_h]     │
│ formatters = [detailed, simple]    │
└────────────────────────────────────┘
         │
         ├─ uses
         │
    ┌────┴───────────────────────┐
    │                             │
    ▼                             ▼
┌───────────────────┐      ┌──────────────────┐
│ file_handler      │      │ console_handler  │
├───────────────────┤      ├──────────────────┤
│ name = "FileH"    │      │ name = "ConsoleH"│
│ level = DEBUG     │      │ level = WARNING  │
│ filename = "..."  │      │ stream = stderr  │
│ maxBytes = 5MB    │      │ format = simple  │
│ backupCount = 5   │      └──────────────────┘
│ format = detailed │
└───────────────────┘
         │
         │ writes_to
         ▼
┌────────────────────────────────────┐
│  weather_app_20251214.log: File    │
├────────────────────────────────────┤
│ location = "logs/"                 │
│ size = 1.2 MB                      │
│ encoding = "utf-8"                 │
│ entries = 1,245                    │
└────────────────────────────────────┘
         │
         │ contains
         ▼
┌────────────────────────────────────┐
│  sample_log_entry: str             │
├────────────────────────────────────┤
│ "2025-12-14 16:15:30,234 -        │
│  WeatherApp - INFO -               │
│  [app.py:245] -                    │
│  Successfully fetched weather      │
│  for London"                       │
└────────────────────────────────────┘
```

---

## Object Diagram 7: Complete Application State

```
Scenario: Full application state at runtime

┌─────────────────────────────┐
│  app: FlaskApplication      │
├─────────────────────────────┤
│ port = 5000                 │
│ debug = True                │
│ running = True              │
└──────────┬──────────────────┘
           │
      ┌────┴────┬──────────┬──────────┬──────────┐
      │          │          │          │          │
      ▼          ▼          ▼          ▼          ▼
   Users    Weather   Forecast   Sessions   Logs
      │          │          │          │          │
      ▼          ▼          ▼          ▼          ▼
┌───────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│john   │ │london    │ │day1...5  │ │john_sess │ │app.log   │
│jane   │ │paris     │ │details   │ │jane_sess │ │errors.log│
│...    │ │new york  │ │...       │ │...       │ │...       │
└───────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘

Active Connections:
┌──────────────────────────────────┐
│  user_client: HttpClient         │
├──────────────────────────────────┤
│ ip = "192.168.1.100"             │
│ session_id = "abc123def"         │
│ last_request = "GET /weather"    │
│ timestamp = "2025-12-14 16:20"   │
└──────────────────────────────────┘
```

---

## Object Relationships

### Aggregation (has-a)
- Weather has Forecast (1 to Many)
- Session has User (1 to 1)
- Logger has Handlers (1 to Many)

### Association (uses)
- Route uses Service
- Service uses Model
- Handler uses Formatter

### Dependency
- API Request depends on HTTP Client
- Response depends on JSON Parser
- Log depends on File System

---

## State Transitions

### User Object States
```
Unregistered → Registered → Authenticated → Logout → Unregistered
    (signup)   (login)     (session)    (logout)
```

### Weather Object States
```
Requested → Fetching → Received → Parsed → Displayed
    │                                         │
    └─────────── Error ─────────────────────┘
```

### Request Object States
```
Created → Validated → Sent → Response Received → Processed
   │                              │
   └────── Timeout ───────────────┘
```

---

## Object Diagram Summary Table

| Object | Type | State | Related Objects |
|--------|------|-------|-----------------|
| user | Model | Active | session, log |
| weather | Model | Current | forecast, map |
| forecast | Model | Future | weather, display |
| session | Service | Active | user, logger |
| logger | Service | Running | handlers, files |
| api_response | Data | Cached | weather, forecast |
| error | Exception | Caught | handler, log |

---

## Runtime Snapshot

**Current Time**: 2025-12-14 16:30:00

**Active Objects**:
- 2 user sessions
- 1 active weather search
- 5 forecast objects loaded
- 3 error logs
- 1 file handler writing
- 1 console handler displaying

**Memory Usage**: ~45 MB
**Log File Size**: 1.2 MB
**Active Connections**: 2

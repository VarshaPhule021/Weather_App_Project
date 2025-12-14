# Use Case Diagram - Weather App (Modular Architecture)

## Overview
The use case diagram shows interactions between users and the system with the new modular architecture emphasizing separation of concerns (UserService, WeatherService).

---

## Use Case Diagram (ASCII)

```
                              ┌──────────────────────────────────────┐
                              │     WEATHER APP SYSTEM               │
                              │  (Modular Architecture)              │
                              └──────────────────────────────────────┘
                                              │
                  ┌─────────────────┬─────────┼─────────┬──────────────────┐
                  │                 │         │         │                  │
                  ▼                 ▼         ▼         ▼                  ▼
            ┌──────────┐      ┌──────────┐  ┌────────┐ ┌──────────┐  ┌──────────┐
            │  Sign Up │      │  Login   │  │ Logout │ │ Search   │  │  View    │
            │ (Register│      │ (Access) │  │        │ │ Weather  │  │ Forecast │
            │   User)  │      │          │  │        │ │          │  │          │
            └──────────┘      └──────────┘  └────────┘ └──────────┘  └──────────┘
                  │                 │          │           │              │
                  └─────────────────┴──────────┴───────────┴──────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
        ┌───────────▼────────┐  ┌──▼──────────┐  ┌─▼────────────────┐
        │  UserService       │  │ Session     │  │ WeatherService   │
        │  (manage users)    │  │ Management  │  │ (fetch weather)  │
        └────────────────────┘  └─────────────┘  └──────────────────┘
                    │                                    │
        ┌───────────┴──────────────────┬────────────────┴─────┐
        │                              │                      │
        ▼                              ▼                      ▼
    ┌─────────────┐          ┌────────────────┐    ┌──────────────────┐
    │ User Model  │          │ WeatherData    │    │ ForecastDay      │
    │ (Dataclass) │          │ Model          │    │ Model            │
    │             │          │ (Dataclass)    │    │ (Dataclass)      │
    │ - email     │          │                │    │                  │
    │ - username  │          │ - city         │    │ - date           │
    │ - password  │          │ - country      │    │ - day            │
    │ - created_at│          │ - temperature  │    │ - temp_max       │
    │             │          │ - humidity     │    │ - temp_min       │
    │ Methods:    │          │ - wind_speed   │    │ - humidity       │
    │ to_dict()   │          │ - ... (20+)    │    │ - description    │
    └─────────────┘          └────────────────┘    └──────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌────────────────┐ ┌──────────────┐ ┌──────────────┐
            │ Fetch Current  │ │ Fetch 5-Day  │ │ Calculate    │
            │ Weather (API)  │ │ Forecast(API)│ │ Wind Dir     │
            │                │ │              │ │              │
            │ Uses requests  │ │ Uses requests│ │ (N, NE, E...)│
            │ library        │ │ library      │ │              │
            └────────────────┘ └──────────────┘ └──────────────┘
                    │               │
                    └───────────────┼───────────────┐
                                    │               │
                                    ▼               ▼
                        ┌────────────────────────────────┐
                        │   OpenWeather API              │
                        │   (External Service)           │
                        │                                │
                        │ - /data/2.5/weather (current)  │
                        │ - /data/2.5/forecast (5-day)   │
                        └────────────────────────────────┘
```

---

## Detailed Use Cases

### 1. User Registration
```
┌──────────────┐
│ New User     │
└────┬─────────┘
     │ initiates
     ▼
┌─────────────────────────────────────────────┐
│ Sign Up (Register User)                     │
├─────────────────────────────────────────────┤
│ Actors: New User                            │
│ System: UserService                         │
│                                             │
│ Flow:                                       │
│ 1. User enters email, username, password    │
│ 2. Flask validates input                    │
│ 3. UserService.register_user() called       │
│ 4. Service validates email uniqueness       │
│ 5. Service hashes password                  │
│ 6. Service saves user to users.json         │
│ 7. Confirmation sent to user                │
│                                             │
│ Preconditions:                              │
│ - User not already registered               │
│ - Valid email format                        │
│ - Password meets requirements               │
│                                             │
│ Postconditions:                             │
│ - User account created                      │
│ - Data persisted to file                    │
│ - User redirected to login                  │
└─────────────────────────────────────────────┘
```

### 2. User Login
```
┌──────────────────┐
│ Registered User  │
└────┬─────────────┘
     │ initiates
     ▼
┌──────────────────────────────────────────────┐
│ Login (Authenticate User)                    │
├──────────────────────────────────────────────┤
│ Actors: User                                 │
│ System: UserService, Session Manager        │
│                                              │
│ Flow:                                        │
│ 1. User enters email and password            │
│ 2. Flask validates input                     │
│ 3. UserService.authenticate_user() called    │
│ 4. Service loads users from users.json       │
│ 5. Service finds user by email               │
│ 6. Service verifies password match           │
│ 7. Session created with user info            │
│ 8. User redirected to /weather               │
│                                              │
│ Preconditions:                               │
│ - User exists in system                      │
│ - Correct credentials provided               │
│                                              │
│ Postconditions:                              │
│ - Session established                        │
│ - User authenticated for requests            │
│ - Access to weather features granted         │
└──────────────────────────────────────────────┘
```

### 3. Search Weather
```
┌─────────────────┐
│ Authenticated   │
│ User            │
└────┬────────────┘
     │ initiates
     ▼
┌──────────────────────────────────────────────┐
│ Search Current Weather                       │
├──────────────────────────────────────────────┤
│ Actors: User                                 │
│ System: WeatherService, OpenWeather API      │
│                                              │
│ Flow:                                        │
│ 1. User enters city name                     │
│ 2. Flask validates session (user logged in)  │
│ 3. Flask validates city input                │
│ 4. WeatherService.get_current_weather()     │
│ 5. Service makes HTTP request to API         │
│ 6. API returns JSON with weather data        │
│ 7. Service creates WeatherData object        │
│ 8. Service calculates wind direction         │
│ 9. Flask renders result.html with data       │
│ 10. User views current weather               │
│                                              │
│ Preconditions:                               │
│ - User authenticated (session active)        │
│ - Valid city name provided                   │
│ - API available and responding               │
│                                              │
│ Postconditions:                              │
│ - Current weather displayed                  │
│ - Data cached in response                    │
│ - Request logged                             │
└──────────────────────────────────────────────┘
```

### 4. View Forecast
```
┌─────────────────┐
│ Authenticated   │
│ User            │
└────┬────────────┘
     │ initiates
     ▼
┌──────────────────────────────────────────────┐
│ View 5-Day Forecast                          │
├──────────────────────────────────────────────┤
│ Actors: User                                 │
│ System: WeatherService, OpenWeather API      │
│                                              │
│ Flow:                                        │
│ 1. User clicks "View Forecast" button        │
│ 2. Flask validates session                   │
│ 3. Flask extracts city from request          │
│ 4. WeatherService.get_forecast() called      │
│ 5. Service makes HTTP forecast API call      │
│ 6. API returns JSON with 40 3-hour entries   │
│ 7. Service extracts first 5 days             │
│ 8. Service creates ForecastDay objects       │
│ 9. Flask renders forecast.html with data     │
│ 10. User views 5-day forecast                │
│                                              │
│ Preconditions:                               │
│ - User authenticated                         │
│ - City selected                              │
│ - API available                              │
│                                              │
│ Postconditions:                              │
│ - 5-day forecast displayed                   │
│ - Daily data shown (temp, humidity, etc.)    │
│ - Request logged                             │
└──────────────────────────────────────────────┘
```

### 5. Logout
```
┌─────────────────┐
│ Authenticated   │
│ User            │
└────┬────────────┘
     │ initiates
     ▼
┌──────────────────────────────────────────────┐
│ Logout (End Session)                         │
├──────────────────────────────────────────────┤
│ Actors: User                                 │
│ System: Flask Session Manager                │
│                                              │
│ Flow:                                        │
│ 1. User clicks "Logout" button               │
│ 2. GET /logout endpoint called               │
│ 3. Flask retrieves session user info         │
│ 4. Flask logs logout event                   │
│ 5. Flask clears session data                 │
│ 6. Flask clears Flask session cookies        │
│ 7. User redirected to /login                 │
│ 8. User viewing login page                   │
│                                              │
│ Preconditions:                               │
│ - User session exists                        │
│ - User authenticated                         │
│                                              │
│ Postconditions:                              │
│ - Session terminated                         │
│ - Cookies cleared                            │
│ - User unauthenticated                       │
│ - Access to /weather blocked                 │
└──────────────────────────────────────────────┘
```

---

## Use Cases Description

### 1. **Sign Up** (UC-001)
- **Actor**: Unregistered User
- **Precondition**: User is not logged in
- **Main Flow**:
  1. User navigates to signup page
  2. User enters username, email, password
  3. System validates input
  4. System checks if email exists
  5. System saves user to users.json
  6. System displays success message
- **Postcondition**: User account created, user can login

### 2. **Login** (UC-002)
- **Actor**: Registered User
- **Precondition**: User has valid account
- **Main Flow**:
  1. User navigates to login page
  2. User enters email and password
  3. System validates credentials
  4. System creates session
  5. System redirects to weather page
- **Alternative Flow**: Invalid credentials → Show error message
- **Postcondition**: User logged in, session created

### 3. **Logout** (UC-003)
- **Actor**: Authenticated User
- **Precondition**: User is logged in
- **Main Flow**:
  1. User clicks logout button
  2. System clears session
  3. System redirects to login page
- **Postcondition**: User logged out, session destroyed

### 4. **Search Weather** (UC-004)
- **Actor**: Authenticated User
- **Precondition**: User is logged in
- **Main Flow**:
  1. User enters city name
  2. System validates input
  3. System calls OpenWeather API
  4. System extracts weather data
  5. System displays weather with 12 metrics
  6. System displays location map
- **Alternative Flow**: City not found → Show error message
- **Postcondition**: Current weather displayed with all details

### 5. **View Forecast** (UC-005)
- **Actor**: Authenticated User
- **Precondition**: User searched for a city
- **Main Flow**:
  1. User clicks "View 5-Day Forecast"
  2. System fetches forecast data
  3. System displays 5 daily forecasts
  4. System shows location map
  5. User can return to weather
- **Postcondition**: Forecast page displayed with all details

### 6. **Fetch Weather Data** (UC-006)
- **Actor**: System
- **Precondition**: API key configured
- **Main Flow**:
  1. System builds API request
  2. System calls OpenWeather API
  3. API returns JSON response
  4. System parses response
  5. System extracts relevant data
- **Exception**: Timeout → Show error, timeout after 10 seconds
- **Exception**: Invalid API response → Show error
- **Postcondition**: Weather data received and parsed

---

## Use Case Relationships

### Extends
- Login extends Authenticate User
- Logout extends Session Management
- Search Weather extends Fetch Weather Data
- View Forecast extends Fetch Weather Data

### Includes
- Search Weather includes Fetch Weather Data
- View Forecast includes Fetch Weather Data
- Fetch Weather Data includes Call OpenWeather API

---

## Actor Definitions

### Primary Actors
1. **User** - Person interacting with the weather app
   - Goals: Get weather information, view forecasts
   - Characteristics: May be registered or anonymous

2. **System** - Backend weather app
   - Goals: Process requests, fetch data, store sessions
   - Characteristics: Automated, always available

### Secondary Actors
1. **OpenWeather API** - External weather data provider
   - Goals: Provide accurate weather data
   - Characteristics: REST API, JSON responses

---

## Use Case Summary Table

| ID | Use Case | Actor | Type | Priority |
|---|---|---|---|---|
| UC-001 | Sign Up | User | Primary | High |
| UC-002 | Login | User | Primary | High |
| UC-003 | Logout | User | Primary | Medium |
| UC-004 | Search Weather | User | Primary | High |
| UC-005 | View Forecast | User | Primary | High |
| UC-006 | Fetch Weather Data | System | Secondary | High |

---

## Business Rules

1. **Authentication**: All weather operations require authentication
2. **Data Validation**: All user inputs must be validated
3. **API Limits**: Requests timeout after 10 seconds
4. **Data Freshness**: Weather data is fetched on-demand (no caching)
5. **Error Handling**: All errors must be caught and logged
6. **User Privacy**: Passwords hashed before storage (planned improvement)

---

## Key Features Represented

✅ User authentication (Sign up, Login, Logout)
✅ Weather search and display
✅ 5-day forecast
✅ Location mapping
✅ Error handling
✅ Session management
✅ API integration

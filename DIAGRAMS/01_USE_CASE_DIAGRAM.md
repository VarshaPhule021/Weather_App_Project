# Use Case Diagram - Weather App

## Overview
The use case diagram shows interactions between users and the system.

---

## Use Case Diagram (ASCII)

```
                                    ┌─────────────────────────┐
                                    │    WEATHER APP SYSTEM   │
                                    └─────────────────────────┘
                                               │
        ┌──────────────────┬──────────────────┼──────────────────┬──────────────────┐
        │                  │                  │                  │                  │
        ▼                  ▼                  ▼                  ▼                  ▼
    ┌────────┐        ┌──────────┐      ┌─────────┐        ┌──────────┐      ┌──────────┐
    │ Sign Up│        │  Login   │      │ Logout  │        │ Search   │      │ View     │
    │        │        │          │      │ Session │        │ Weather  │      │ Forecast │
    └────────┘        └──────────┘      └─────────┘        └──────────┘      └──────────┘
        │                  │                  │                  │                  │
        └──────────────────┴──────────────────┴──────────────────┴──────────────────┘
                                       │
                                       │ extends/uses
                                       ▼
                          ┌────────────────────────┐
                          │   Authenticate User    │
                          │   (Login Required)     │
                          └────────────────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
            ┌────────────────┐  ┌────────────────┐  ┌──────────────┐
            │ Fetch Current  │  │ Fetch 5-Day    │  │ Display      │
            │ Weather Data   │  │ Forecast       │  │ Location Map │
            │ (API Call)     │  │ (API Call)     │  │ (Leaflet.js) │
            └────────────────┘  └────────────────┘  └──────────────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                                       ▼
                          ┌────────────────────────┐
                          │  Call OpenWeather API  │
                          │  (External Service)    │
                          └────────────────────────┘
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

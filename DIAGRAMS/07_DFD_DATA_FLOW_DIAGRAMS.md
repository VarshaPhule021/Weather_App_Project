# DFD (Data Flow Diagram) - Weather App (Modular Architecture)

## Overview
Data Flow Diagrams (DFD) show how data moves through the system at different levels of abstraction with the new modular architecture.

---

## DFD Level 0 (Context Diagram)

```
                           ┌──────────────────────────┐
                           │    WEATHER APP SYSTEM    │
                           │   (Black Box - Level 0)  │
                           └──────────┬───────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
   ┌─────────┐                  ┌──────────────┐            ┌──────────────┐
   │  USER   │                  │  OPENWEATHER │            │   FILE       │
   │         │◄────────────────►│     API      │            │  SYSTEM      │
   │         │ User Input/      │ (REST API)   │            │  (JSON)      │
   │         │ Display Output   │              │            │              │
   │         │                  │ Real-time    │            │ Persistent   │
   │         │                  │ Weather Data │            │ User Data    │
   └─────────┘                  └──────────────┘            └──────────────┘
        │                             │                             │
        │                             │                             │
        │  1. Login/Signup            │  2. Fetch Weather Data      │  3. Load/Save
        │  2. Search Weather          │  3. Fetch Forecast         │     User Info
        │  3. View Forecast           │                            │
        │  4. View Map                │                            │
        │  5. Logout                  │                            │
        │                             │                            │
```

**External Entities**:
- **User**: Interacts with the system (login, search, view data)
- **OpenWeather API**: Provides real-time weather data
- **File System**: Stores user information (users.json)

---

## DFD Level 1 (Major Processes)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WEATHER APP SYSTEM (Level 1)                        │
└─────────────────────────────────────────────────────────────────────────────┘

        USER
         │
         ▼
┌─────────────────────────────────────┐
│  P1: Authentication Management      │
├─────────────────────────────────────┤
│  - Validate user input              │
│  - Check credentials                │
│  - Manage sessions                  │
│  - Load/save users                  │
└─────────────────────────────────────┘
         │
         ├──────────────────────────────────────┐
         │                                      │
         ▼                                      ▼
    User Data                         Session Info
    (users.json)                      (in memory)
         │                                      │
         │                                      │
         │◄─────────────────────────────────────┤
         │                                      │
         ▼                                      ▼
┌──────────────────────────────────┐  ┌─────────────────────────┐
│ P2: Weather Management           │  │ P3: Session Validation  │
├──────────────────────────────────┤  ├─────────────────────────┤
│ - Validate city input            │  │ - Check session active  │
│ - Format API request             │  │ - Verify user logged in │
│ - Parse API response             │  │ - Handle timeout        │
│ - Extract weather data           │  │ - Log activities        │
│ - Generate map                   │  └─────────────────────────┘
└──────────────────────────────────┘
         │
         ├──────────────────────┐
         │                      │
         ▼                      ▼
    OpenWeather API          Logs
    (REST API)               (log files)
         │                      │
         │                      │
         ▼                      ▼
┌──────────────────────────────────┐  ┌─────────────────────────┐
│ P4: Data Transformation          │  │ P5: Logging             │
├──────────────────────────────────┤  ├─────────────────────────┤
│ - Extract temperature            │  │ - Log user actions      │
│ - Extract wind direction         │  │ - Log errors            │
│ - Process forecast (5-day)       │  │ - Log API calls         │
│ - Format for display             │  │ - Store in files        │
└──────────────────────────────────┘  └─────────────────────────┘
         │                                      │
         ▼                                      ▼
    Weather Display                        Log Records
    (HTML/Maps)                            (logs/*.log)
         │                                      │
         │◄─────────────────────────────────────┤
         │
         ▼
       USER
```

---

## DFD Level 2: Authentication Process (P1 Decomposed)

```
┌──────────────────────────────────────────────────────────────┐
│           P1: Authentication Management (Level 2)             │
└──────────────────────────────────────────────────────────────┘

INPUT FLOWS:
  ├─ Username/Email
  ├─ Password
  ├─ Form Action (Login/Signup)
  └─ Session Data (if exists)

┌─────────────────────────────────┐
│ P1.1: Input Validation          │
├─────────────────────────────────┤
│ Check for:                      │
│ - Empty fields                  │
│ - Email format                  │
│ - Password strength             │
│ - Password confirmation match   │
└──────────┬──────────────────────┘
           │
           ├─ Valid? ──→ Continue
           │
           └─ Invalid? ──→ Return Error
                            (UI Display)

┌─────────────────────────────────┐
│ P1.2: Load Existing Users       │
├─────────────────────────────────┤
│ - Read users.json               │
│ - Parse JSON                    │
│ - Cache in memory               │
└──────────┬──────────────────────┘
           │
    ┌──────▼────────┐
    │               │
    ▼               ▼
 LOGIN          SIGNUP
    │               │
    ▼               ▼
┌─────────────┐  ┌─────────────┐
│ P1.3.A:     │  │ P1.3.B:     │
│ Verify User │  │ Create User │
├─────────────┤  ├─────────────┤
│ - Check if  │  │ - Check if  │
│   email     │  │   email     │
│   exists    │  │   unique    │
│ - Check pwd │  │ - Hash pwd  │
│ - Generate │  │ - Add to    │
│   session   │  │   users dict│
└────┬────────┘  └────┬────────┘
     │                │
     ├─ Success ──→ ├─ Save to File
     │                │
     └─ Failure ──→ └─ Return Error

┌─────────────────────────────────┐
│ P1.4: Save Users (if modified)  │
├─────────────────────────────────┤
│ - Serialize to JSON             │
│ - Write to users.json           │
│ - Handle file errors            │
└──────────┬──────────────────────┘
           │
           ▼
     FILE SYSTEM
     (users.json)

┌─────────────────────────────────┐
│ P1.5: Session Management        │
├─────────────────────────────────┤
│ - Create session ID             │
│ - Store user email/username     │
│ - Set timeout                   │
│ - Return session cookie         │
└──────────┬──────────────────────┘
           │
           ▼
    SESSION DATA
    (in memory)

OUTPUT FLOWS:
  ├─ Session ID (if success)
  ├─ Success/Error Message
  └─ User Redirect Path
```

---

## DFD Level 2: Weather Process (P2 Decomposed)

```
┌──────────────────────────────────────────────────────────────┐
│            P2: Weather Management (Level 2)                  │
└──────────────────────────────────────────────────────────────┘

INPUT FLOWS:
  ├─ City Name (from User)
  ├─ Session Token (validation)
  └─ API Key (configuration)

┌─────────────────────────────────┐
│ P2.1: Input Validation          │
├─────────────────────────────────┤
│ - City name not empty           │
│ - Check session valid           │
│ - Verify user authenticated     │
└──────────┬──────────────────────┘
           │
           ├─ Valid? ──→ Continue
           │
           └─ Invalid? ──→ Error Response

┌─────────────────────────────────┐
│ P2.2: Format API Request        │
├─────────────────────────────────┤
│ - Build URL                     │
│ - Set parameters:               │
│   * q = city name               │
│   * appid = API key             │
│   * units = metric              │
│ - Set timeout = 10 seconds      │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ P2.3: Call OpenWeather API      │
├─────────────────────────────────┤
│ - Make HTTP GET request         │
│ - Wait for response (max 10s)   │
│ - Handle timeout                │
│ - Handle HTTP errors            │
└──────────┬──────────────────────┘
           │
      ┌────┴────┐
      │          │
   Success     Timeout/Error
      │          │
      ▼          ▼
   JSON    ┌──────────────┐
   Data    │ P2.6: Log    │
      │    │ Error        │
      │    └──────┬───────┘
      │           │
      ▼           ▼
┌──────────────────────────────────┐
│ P2.4: Parse & Extract Data       │
├──────────────────────────────────┤
│ - Parse JSON response            │
│ - Extract temperature            │
│ - Extract humidity               │
│ - Extract wind data              │
│ - Extract coordinates            │
│ - Format for display             │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ P2.5: Get Forecast (5-day)       │
├──────────────────────────────────┤
│ - Similar process to weather     │
│ - Call separate API endpoint     │
│ - Extract 5 daily forecasts      │
│ - Process each day               │
└──────────┬───────────────────────┘
           │
      ┌────┴────┐
      │          │
   Success     Error
      │          │
      ▼          ▼
 Forecast    Error Log
   Data         │
      │         │
      └────┬────┘
           │
           ▼
┌──────────────────────────────────┐
│ P2.6: Build Location Map         │
├──────────────────────────────────┤
│ - Get latitude/longitude         │
│ - Initialize Leaflet map         │
│ - Set zoom level                 │
│ - Add marker                     │
│ - Generate HTML                  │
└──────────┬───────────────────────┘
           │
           ▼
       MAP DATA
    (HTML/JS)

OUTPUT FLOWS:
  ├─ Weather Data (formatted)
  ├─ Forecast Data (5 days)
  ├─ Map HTML
  ├─ Success/Error Message
  └─ Log Entry (audit trail)
```

---

## DFD Level 2: Logging Process (P5 Decomposed)

```
┌──────────────────────────────────────────────────────────────┐
│               P5: Logging System (Level 2)                    │
└──────────────────────────────────────────────────────────────┘

INPUT FLOWS:
  ├─ Log Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  ├─ Message Text
  ├─ Context (user, file, line number)
  └─ Timestamp

┌─────────────────────────────────┐
│ P5.1: Log Level Determination   │
├─────────────────────────────────┤
│ - Classify event severity       │
│ - DEBUG: Detailed info          │
│ - INFO: Normal operation        │
│ - WARNING: Potential issue      │
│ - ERROR: Operation failed       │
│ - CRITICAL: System failure      │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ P5.2: Format Log Message        │
├─────────────────────────────────┤
│ - Add timestamp                 │
│ - Add logger name               │
│ - Add log level                 │
│ - Add source location           │
│ - Add message text              │
│ Format:                         │
│ YYYY-MM-DD HH:MM:SS - NAME -   │
│ LEVEL - [file:line] - MESSAGE   │
└──────────┬──────────────────────┘
           │
           ▼
      ┌────┴─────┬──────────┐
      │           │          │
      ▼           ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ P5.3:    │ │ P5.4:    │ │ P5.5:    │
│ File     │ │ Console  │ │ Database │
│ Handler  │ │ Handler  │ │ Handler  │
├──────────┤ ├──────────┤ ├──────────┤
│ Write to │ │ Print to │ │ Store    │
│ log file │ │ stderr   │ │ in DB    │
│ Rotate   │ │ (if      │ │ (future) │
│ when 5MB │ │ WARNING+)│ │          │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     ▼            ▼            ▼
 LOG FILE    CONSOLE    DATABASE
 logs/*.log  OUTPUT     (logs table)

┌─────────────────────────────────┐
│ P5.6: Handle Rotation           │
├─────────────────────────────────┤
│ Check file size:                │
│ - If > 5MB:                     │
│   * Rename current file         │
│   * Create new log file         │
│   * Keep 5 backup files         │
│   * Delete old files            │
└─────────────────────────────────┘

OUTPUT FLOWS:
  ├─ Log File Entry
  ├─ Console Output
  ├─ Database Record (planned)
  └─ Audit Trail Data
```

---

## DFD Level 3: Data Transform Example (P4 Decomposed)

```
┌──────────────────────────────────────────────────────────────┐
│          P4: Data Transformation (Level 3)                    │
└──────────────────────────────────────────────────────────────┘

INPUT: Raw JSON from OpenWeather API

{
  "name": "London",
  "sys": {"country": "GB"},
  "main": {"temp": 12.5, "humidity": 75},
  "wind": {"speed": 3.5, "deg": 270},
  ...
}

┌──────────────────────────────────┐
│ P4.1: Extract Basic Info         │
├──────────────────────────────────┤
│ - City: London                   │
│ - Country: GB                    │
│ - Latitude: 51.5074              │
│ - Longitude: -0.1278             │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ P4.2: Temperature Processing     │
├──────────────────────────────────┤
│ - Current: 12.5°C                │
│ - Feels like: 10.2°C             │
│ - Min: 8.3°C                     │
│ - Max: 15.1°C                    │
│ Round to 1 decimal place         │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ P4.3: Wind Processing            │
├──────────────────────────────────┤
│ - Speed: 3.5 m/s                 │
│ - Direction: 270° (West)         │
│ - Gust: 5.2 m/s                  │
│ - Convert degrees to compass     │
│   270° = West (W)                │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ P4.4: Condition Processing       │
├──────────────────────────────────┤
│ - Main: Cloudy                   │
│ - Description: Overcast Clouds   │
│ - Icon: 04d                      │
│ - Humidity: 75%                  │
│ - Pressure: 1013 hPa             │
│ - Visibility: 10 km              │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ P4.5: Precipitation Processing   │
├──────────────────────────────────┤
│ - Rain: 0.0 mm                   │
│ - Snow: 0.0 mm                   │
│ - Cloudiness: 60%                │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ P4.6: Time Processing            │
├──────────────────────────────────┤
│ - Sunrise: 7:30 AM               │
│ - Sunset: 4:15 PM                │
│ - Convert from UNIX timestamp    │
└──────────┬───────────────────────┘
           │
           ▼
OUTPUT: Formatted Weather Dictionary
{
  "city": "London",
  "country": "GB",
  "temperature": 12.5,
  "feels_like": 10.2,
  "humidity": 75,
  "wind_direction": "W",
  "sunrise": "7:30 AM",
  ...
}
```

---

## Data Flow Summary

### Data Stores

| Store | Type | Contents | Access |
|-------|------|----------|--------|
| DS1: users.json | File | User credentials, usernames | Read/Write |
| DS2: Session Memory | Memory | Active user sessions | Read/Write |
| DS3: logs/* | Files | Application events, errors | Write/Read |
| D4: Weather Cache | Memory | Current weather results | Read/Write |

### Data Flows

| Flow | Source | Destination | Content |
|------|--------|-------------|---------|
| DF1 | User | P1 | Login/Signup data |
| DF2 | P1 | User | Session/Error |
| DF3 | P2 | OpenWeather | API Request |
| DF4 | OpenWeather | P2 | Weather JSON |
| DF5 | P2 | User | Weather display |
| DF6 | P2-P5 | Logs | Log entries |
| DF7 | P1 | DS1 | User data |
| DF8 | DS1 | P1 | User data |

---

## DFD Characteristics

### Balanced Flow
- All inputs have corresponding outputs
- Data storage is consistent
- Processes transform inputs to outputs

### Abstraction Levels
- **Level 0**: Single process (entire system)
- **Level 1**: Major business processes
- **Level 2**: Detailed processes
- **Level 3**: Specific algorithms/transforms

### Key Features
✅ Shows data movement
✅ Identifies data stores
✅ Clarifies process boundaries
✅ Reveals data dependencies
✅ Helps with validation

---

## Summary

The DFD shows:
- 5 major processes (P1-P5)
- 3 external entities
- 4 data stores
- Multiple data flows
- Clear data transformations
- Error handling paths
- Logging integration

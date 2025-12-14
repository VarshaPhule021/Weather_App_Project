# Activity Diagram - Weather App (Modular Architecture)

## Overview
Activity diagrams show the flow of activities and decisions in the system with the new modular architecture emphasizing service layer interactions.

---

## Activity Diagram 1: User Registration Flow

```
                            START
                             │
                             ▼
                    ┌──────────────────┐
                    │  User Navigates  │
                    │  to Signup Page  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display Signup   │
                    │ Form             │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User Enters      │
                    │ Email, Username, │
                    │ Password         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Submit Form      │
                    │ (POST /signup)   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Flask validates  │
                    │ Input (non-empty)│
                    └─────┬──────┬─────┘
                          │      │
                      Valid   Invalid
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Return Error     │
                          │  │ Message to User  │
                          │  └────┬─────────────┘
                          │       │
                          │       └──→ [Re-display Form]
                          │
                          ▼
                    ┌──────────────────┐
                    │ Call UserService │
                    │ .register_user() │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ UserService:     │
                    │ Load users.json  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Check if email   │
                    │ already exists   │
                    └─────┬──────┬─────┘
                          │      │
                      Unique  Exists
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Return False     │
                          │  │ (Email taken)    │
                          │  └────┬─────────────┘
                          │       │
                          │       ▼
                          │  ┌──────────────────┐
                          │  │ Flask returns    │
                          │  │ error page       │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────┐
                    │ Hash password    │
                    │ (security)       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Create User      │
                    │ object           │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Save to users.   │
                    │ json file        │
                    └─────┬──────┬─────┘
                          │      │
                      Success  Failure
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Log Error        │
                          │  │ Return False     │
                          │  └─────────────────┘
                          │
                          ▼
                    ┌──────────────────┐
                    │ Log registration │
                    │ (INFO level)     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Flask redirects  │
                    │ to login page    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display success  │
                    │ message          │
                    └────────┬─────────┘
                             │
                             ▼
                           END
```

---

## Activity Diagram 2: User Login Flow

```
                            START
                             │
                             ▼
                    ┌──────────────────┐
                    │  User Navigates  │
                    │   to Login Page  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display Login    │
                    │ Form             │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User Enters      │
                    │ Email & Password │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Submit Form      │
                    │ (POST /login)    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Flask validates  │
                    │ Input (non-empty)│
                    └─────┬──────┬─────┘
                          │      │
                      Valid   Invalid
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Return Error     │
                          │  │ Page (400)       │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────────┐
                    │ Call UserService     │
                    │ .authenticate_user() │
                    └────────┬─────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ UserService:     │
                    │ Load users.json  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Find user by     │
                    │ email            │
                    └─────┬──────┬─────┘
                          │      │
                      Found   Not Found
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Log WARNING      │
                          │  │ Return None      │
                          │  └────┬─────────────┘
                          │       │
                          │       ▼
                          │  ┌──────────────────┐
                          │  │ Flask returns    │
                          │  │ error page       │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────┐
                    │ Verify password  │
                    │ (hash match)     │
                    └─────┬──────┬─────┘
                          │      │
                      Match  No Match
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Log WARNING      │
                          │  │ Return None      │
                          │  └────┬─────────────┘
                          │       │
                          │       ▼
                          │  ┌──────────────────┐
                          │  │ Flask returns    │
                          │  │ error page       │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────┐
                    │ Create User      │
                    │ object           │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Return User to   │
                    │ Flask            │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Create Session   │
                    │ (session_obj)    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Create Session   │
                    │ model            │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Set session      │
                    │ in cookies       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Log INFO         │
                    │ "Login success"  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Flask redirects  │
                    │ to /weather      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display weather  │
                    │ search page      │
                    └────────┬─────────┘
                             │
                             ▼
                           END
```

---

## Activity Diagram 3: Weather Search Flow

```
                            START
                             │
                             ▼
                    ┌──────────────────┐
                    │ User on          │
                    │ /weather page    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Check Session    │
                    │ (authenticated?) │
                    └─────┬──────┬─────┘
                          │      │
                      Valid   Invalid
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Redirect to      │
                          │  │ /login           │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────┐
                    │ User enters      │
                    │ city name        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Submit form      │
                    │ (POST /weather)  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Flask validates  │
                    │ city input       │
                    └─────┬──────┬─────┘
                          │      │
                      Valid   Invalid
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Return error     │
                          │  │ page (400)       │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────────────┐
                    │ Call WeatherService      │
                    │ .get_current_weather()   │
                    └────────┬─────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ WeatherService:  │
                    │ Make HTTP GET to │
                    │ OpenWeather API  │
                    └─────┬──────┬─────┘
                          │      │
                      Success Timeout/Error
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Log ERROR        │
                          │  │ Return None      │
                          │  └────┬─────────────┘
                          │       │
                          │       ▼
                          │  ┌──────────────────┐
                          │  │ Flask returns    │
                          │  │ error page       │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────┐
                    │ Parse JSON       │
                    │ response         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Create           │
                    │ WeatherData obj  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Calculate wind   │
                    │ direction from   │
                    │ degrees          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────────────┐
                    │ Call WeatherService      │
                    │ .get_forecast()          │
                    └────────┬─────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ WeatherService:  │
                    │ Make HTTP GET to │
                    │ Forecast API     │
                    └─────┬──────┬─────┘
                          │      │
                      Success Timeout/Error
                          │      │
                          │      ▼
                          │  ┌──────────────────┐
                          │  │ Log ERROR        │
                          │  │ Return None      │
                          │  └────┬─────────────┘
                          │       │
                          │       ▼
                          │  ┌──────────────────┐
                          │  │ Flask renders    │
                          │  │ with only current│
                          │  │ weather          │
                          │  └──────────────────┘
                          │
                          ▼
                    ┌──────────────────┐
                    │ Parse JSON       │
                    │ response         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Extract 5 days   │
                    │ of forecast      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Create           │
                    │ ForecastDay objs │
                    │ for each day     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Log INFO         │
                    │ "Weather fetched"│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Flask renders    │
                    │ result.html with │
                    │ all data         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display weather  │
                    │ & forecast to    │
                    │ user             │
                    └────────┬─────────┘
                             │
                             ▼
                           END
```

---

## Activity Diagram 4: Logout Flow

```
                            START
                             │
                             ▼
                    ┌──────────────────┐
                    │ User clicks      │
                    │ Logout button    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ GET /logout      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Flask gets       │
                    │ user from session│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Log INFO         │
                    │ "User logged out"│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Clear session    │
                    │ dict             │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Clear Flask      │
                    │ session cookie   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Redirect to      │
                    │ /login           │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display login    │
                    │ page             │
                    └────────┬─────────┘
                             │
                             ▼
                           END
```

---
                          │              │
                          ▼              ▼
                    ┌──────────────┐  ┌──────────┐
                    │ Load Users   │  │ Return   │
                    │ from File    │  │ to Form  │
                    └─────┬────────┘  └──────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │ Check Email  │
                    │ & Password   │
                    └─────┬────┬───┘
                          │    │
                        Match   No Match
                          │    │
                          │    ▼
                          │ ┌──────────────┐
                          │ │ Show Invalid │
                          │ │ Credentials  │
                          │ └────┬─────────┘
                          │      │
                          │      └──────────┐
                          │                 │
                          ▼                 ▼
                    ┌──────────────┐    ┌──────────┐
                    │ Create       │    │ Return   │
                    │ Session      │    │ to Form  │
                    └─────┬────────┘    └──────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │ Log Success  │
                    │ Event        │
                    └─────┬────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │ Redirect to  │
                    │ Weather Page │
                    └─────┬────────┘
                          │
                          ▼
                        END
```

---

## Activity Diagram 2: Weather Search Flow

```
                            START
                             │
                             ▼
                    ┌──────────────────┐
                    │ User on Weather  │
                    │ Search Page      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User Enters City │
                    │ Name             │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Submit Search    │
                    │ Form             │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Validate City    │
                    │ Input            │
                    └─────┬──────┬─────┘
                          │      │
                        Valid  Invalid
                          │      │
                          │      ▼
                          │  ┌──────────────┐
                          │  │ Show Error   │
                          │  │ Message      │
                          │  └──────┬───────┘
                          │         │
                          │         └──────┐
                          │                │
                          ▼                ▼
                    ┌──────────────┐    ┌──────────┐
                    │ Call Weather │    │ Return   │
                    │ API          │    │ to Form  │
                    └─────┬────────┘    └──────────┘
                          │
                          ▼
          ┌───────────────────────────┐
          │ Check Response Status     │
          └─┬───────────────────────┬─┘
            │                       │
         Success                   Error
            │                       │
            ▼                       ▼
    ┌──────────────┐         ┌──────────────┐
    │ Parse JSON   │         │ Log Error    │
    │ Response     │         │ (Timeout/API)│
    └────┬─────────┘         └──────┬───────┘
         │                          │
         ▼                          ▼
    ┌──────────────┐         ┌──────────────┐
    │ Extract      │         │ Show User    │
    │ Weather Data │         │ Error Page   │
    └────┬─────────┘         └──────┬───────┘
         │                          │
         ▼                          ▼
    ┌──────────────┐         ┌──────────────┐
    │ Get Forecast │         │ Return to    │
    │ Data         │         │ Search Page  │
    └────┬─────────┘         └──────────────┘
         │
         ▼
    ┌──────────────┐
    │ Extract      │
    │ Forecast Data│
    └────┬─────────┘
         │
         ▼
    ┌──────────────┐
    │ Build Map    │
    │ Coordinates  │
    └────┬─────────┘
         │
         ▼
    ┌──────────────┐
    │ Render Result│
    │ Page with:   │
    │ - Weather    │
    │ - Forecast   │
    │ - Map        │
    └────┬─────────┘
         │
         ▼
    ┌──────────────┐
    │ Log Success  │
    │ Event        │
    └────┬─────────┘
         │
         ▼
        END
```

---

## Activity Diagram 3: Sign Up Flow

```
                            START
                             │
                             ▼
                    ┌──────────────────┐
                    │  User Navigates  │
                    │   to Sign Up     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display Sign Up  │
                    │ Form             │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User Enters:     │
                    │ - Username       │
                    │ - Email          │
                    │ - Password       │
                    │ - Confirm Pass   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Submit Form      │
                    └────────┬─────────┘
                             │
                             ▼
            ┌────────────────────────┐
            │ Validate All Fields    │
            │ (Not Empty)            │
            └─┬──────────────────┬───┘
              │                  │
            Valid              Invalid
              │                  │
              ▼                  ▼
        ┌──────────────┐   ┌──────────────┐
        │ Check Pass   │   │ Show Error   │
        │ Match        │   │ Message      │
        └─┬────────┬───┘   └──────┬───────┘
          │        │             │
        Match   Mismatch        │
          │        │            │
          ▼        ▼            │
    ┌──────────┐ ┌─────────┐   │
    │ Check    │ │ Show    │   │
    │ Pass     │ │ Error:  │   │
    │ Length   │ │ Pass    │   │
    │ (6+ char)│ │ Mismatch│   │
    └─┬────┬───┘ └────┬────┘   │
      │    │          │        │
     Pass Fail        │        │
      │    │          │        │
      ▼    ▼          │        │
  ┌──────┐ │          │        │
  │Check │ │          │        │
  │Email │ │          │        │
  │Exists│ │          │        │
  └┬──┬──┘ │          │        │
    │  │   │          │        │
   No Yes  │          │        │
    │  │   │          │        │
    ▼  ▼   ▼          ▼        ▼
  ┌──────┐┌──┐    ┌──────────────┐
  │Save  ││Show   │Return to Form│
  │User  ││Error: └──────┬───────┘
  │to    ││Email        │
  │File  ││Exists       │
  └┬──┬──┘└──┘          │
    │ │                │
    │ └────────┬───────┘
    │          │
    ▼          ▼
┌──────────┐ ┌──────────┐
│ Log User │ │ Return   │
│ Created  │ │ to Form  │
└────┬─────┘ └──────────┘
     │
     ▼
  ┌──────────┐
  │ Show     │
  │ Success  │
  │ Message  │
  └────┬─────┘
       │
       ▼
     END
```

---

## Activity Diagram 4: View Forecast Flow

```
                            START
                             │
                             ▼
                    ┌──────────────────┐
                    │ User on Weather  │
                    │ Result Page      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User Clicks      │
                    │ "View Forecast"  │
                    │ Button           │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Get City Name    │
                    │ from Query Param │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Validate City    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Call Forecast    │
                    │ API              │
                    └────────┬─────────┘
                             │
                             ▼
          ┌──────────────────────────┐
          │ Check API Response       │
          └─┬──────────────────────┬─┘
            │                      │
         Success                 Error
            │                      │
            ▼                      ▼
    ┌──────────────┐      ┌──────────────┐
    │ Parse JSON   │      │ Log Error    │
    │ Forecast Data│      │ Event        │
    └────┬─────────┘      └──────┬───────┘
         │                       │
         ▼                       ▼
    ┌──────────────┐      ┌──────────────┐
    │ Extract 5    │      │ Show Error   │
    │ Daily Items  │      │ Page         │
    └────┬─────────┘      └──────┬───────┘
         │                       │
         ▼                       ▼
    ┌──────────────┐      ┌──────────────┐
    │ Process Each │      │ Return to    │
    │ Day Data     │      │ Weather Page │
    └────┬─────────┘      └──────────────┘
         │
         ▼
    ┌──────────────┐
    │ Extract City │
    │ Coordinates  │
    └────┬─────────┘
         │
         ▼
    ┌──────────────┐
    │ Render       │
    │ Forecast Page:
    │ - 5 Day Cards
    │ - Location Map
    │ - Navigation  
    └────┬─────────┘
         │
         ▼
    ┌──────────────┐
    │ Log Success  │
    │ Event        │
    └────┬─────────┘
         │
         ▼
        END
```

---

## Swimming Lanes Activity Diagram

```
User          │  System                │  OpenWeather API
──────────────┼──────────────────────────┼──────────────
              │                          │
    Search    │                          │
    Weather   │                          │
       │      │                          │
       ▼      │                          │
    Enter     │                          │
    City      │                          │
       │      │                          │
       └─────→│ Validate Input           │
              │ (Empty, Special Chars)   │
              │                          │
              ├─ Valid ────┐             │
              │            │             │
              │            ├────────────→│ GET /weather?q=city
              │            │             │
              │            │             ├─ Parse
              │            │             │
              │            │←─ 200 OK ───┤
              │            │   JSON Data │
              │            │             │
              │            ├────────────→│ GET /forecast?q=city
              │            │             │
              │            │             ├─ Parse
              │            │             │
              │            │←─ 200 OK ───┤
              │            │   JSON Data │
              │            │             │
              │            ├─ Extract Data
              │            │
              │            ├─ Build Map
              │            │
              │←─ Result ───┤
              │  Page       │
              │             │
       ┌──────┴────────────┐│
       │ View Results      ││
       │ - Weather Data    ││
       │ - Forecast Cards  ││
       │ - Location Map    ││
       └──────────────────┘│
```

---

## Key Decision Points

| Decision | Options | Action |
|----------|---------|--------|
| Input Valid? | Yes / No | Proceed / Show Error |
| User Exists? | Yes / No | Login / Register First |
| API Response OK? | 200 / Error | Parse Data / Show Error |
| Password Match? | Yes / No | Create Account / Retry |
| City Found? | Yes / No | Display Results / Show Error |

---

## Activity States

**Initial States**:
- Start: Application launch
- User Login: User not authenticated

**Activity States**:
- Validate Input: Checking user entries
- Fetch Data: API call in progress
- Process Response: Parsing JSON
- Display Result: Rendering UI

**Final States**:
- End: Activity complete
- Error State: Error occurred
- Success State: Operation successful

---

## Transitions

- **Precondition**: User is logged in
- **Postcondition**: Activity completed or error shown
- **Guard Conditions**: Input validation, API availability
- **Exceptions**: Timeout, API error, invalid data

# Activity Diagram - Weather App

## Overview
Activity diagrams show the flow of activities and decisions in the system.

---

## Activity Diagram 1: User Login Flow

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
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Validate Input   │
                    │ (Empty Check)    │
                    └─────┬──────┬─────┘
                          │      │
                      Valid   Invalid
                          │      │
                          │      ▼
                          │  ┌──────────────┐
                          │  │ Show Error   │
                          │  │ Message      │
                          │  └────┬─────────┘
                          │       │
                          │       └──────┐
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

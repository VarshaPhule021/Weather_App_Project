# Sequence Diagram - Weather App

## Overview
Sequence diagrams show the interactions between objects over time in a specific scenario.

---

## Sequence Diagram 1: User Login Flow

```
User            Browser         Flask App       UserService        Logger
 │                │                │                │                │
 │─ Enter Email──→│                │                │                │
 │ & Password     │                │                │                │
 │                │                │                │                │
 │                │─ POST /login──→│                │                │
 │                │   (email, pwd) │                │                │
 │                │                │                │                │
 │                │                │─ Validate───→  │                │
 │                │                │ Input          │                │
 │                │                │                │                │
 │                │                │─ Load Users─→  │                │
 │                │                │                │─ Read File    │
 │                │                │                │    (users.json)
 │                │                │                │←─ Return Users─│
 │                │                │←─ Users Dict───│                │
 │                │                │                │                │
 │                │                │─ Verify──────→ │                │
 │                │                │ Credentials    │                │
 │                │                │                │                │
 │                │                │                │─ Log Info─────→│
 │                │                │                │   "Successful  │
 │                │                │                │   login"       │
 │                │                │                │                │
 │                │                │─ Create Session│                │
 │                │                │                │                │
 │                │←─ 302 Redirect─│                │                │
 │                │ /weather       │                │                │
 │                │                │                │                │
 │←─ Redirect───┤ │                │                │                │
 │ to Weather   │ │                │                │                │
 │              │                  │                │                │
 ▼              ▼                  ▼                ▼                ▼
```

---

## Sequence Diagram 2: Weather Search Flow

```
User         Browser       Flask App       WeatherAPI      Logger
 │              │              │               │              │
 │─ Search ────→│              │               │              │
 │  City: London│              │               │              │
 │              │              │               │              │
 │              │─ POST /────→ │               │              │
 │              │  weather    │               │              │
 │              │  (city name)│               │              │
 │              │              │               │              │
 │              │              │─ Validate───→│              │
 │              │              │  City Input  │              │
 │              │              │              │              │
 │              │              │─ Check──────→│              │
 │              │              │  Session    │              │
 │              │              │ (Authenticated)
 │              │              │              │              │
 │              │              │─────────────→│ GET /weather│
 │              │              │  ?q=London   │ ?appid=KEY  │
 │              │              │              │              │
 │              │              │              │← 200 JSON ──│
 │              │              │←─────────────│ (Weather   │
 │              │              │   Data      │  Data)      │
 │              │              │              │              │
 │              │              │─ Extract───→│              │
 │              │              │  Data       │              │
 │              │              │              │              │
 │              │              │──────────────────────────→│
 │              │              │  Log Success              │
 │              │              │  Event                    │
 │              │              │              │              │
 │              │              │─ Get──────→ │              │
 │              │              │  Forecast   │              │
 │              │              │──────────────────→ GET /───│
 │              │              │            forecast│q=London
 │              │              │            ──────→│         │
 │              │              │              │← 200 JSON ──│
 │              │              │←─────────────│ (Forecast  │
 │              │              │   Data)     │  Data)      │
 │              │              │              │              │
 │              │              │─ Extract───→│              │
 │              │              │  Forecast   │              │
 │              │              │              │              │
 │              │              │─ Build Map──│              │
 │              │              │              │              │
 │              │←─ Render ────│              │              │
 │              │  result.html │              │              │
 │              │  with data   │              │              │
 │              │              │              │              │
 │←─ Display ───│              │              │              │
 │  Weather     │              │              │              │
 │  Results     │              │              │              │
 │              │              │              │              │
 ▼              ▼              ▼              ▼              ▼
```

---

## Sequence Diagram 3: Sign Up Flow

```
User         Browser        Flask App        UserService        Logger
 │              │               │               │                │
 │─ Click ─────→│               │               │                │
 │  Sign Up     │               │               │                │
 │              │               │               │                │
 │              │─ Show Form───→│               │                │
 │              │               │               │                │
 │─ Fill Form──→│               │               │                │
 │  (details)   │               │               │                │
 │              │               │               │                │
 │              │─ POST /signup│               │                │
 │              │  (form data)  │               │                │
 │              │               │               │                │
 │              │               │─ Validate───→ │                │
 │              │               │  Input       │                │
 │              │               │  (empty,     │                │
 │              │               │   length)    │                │
 │              │               │               │                │
 │              │               │─ Check Pass──→│                │
 │              │               │  Match       │                │
 │              │               │               │                │
 │              │               │─ Load Users──→│                │
 │              │               │               │─ Read File     │
 │              │               │               │  (users.json)  │
 │              │               │               │← Return Users──│
 │              │               │←─ Users Dict──│                │
 │              │               │               │                │
 │              │               │─ Check Email─→│                │
 │              │               │  Exists      │                │
 │              │               │               │                │
 │              │               │─ Save User──→ │                │
 │              │               │               │─ Write File    │
 │              │               │               │  (users.json)  │
 │              │               │               │                │
 │              │               │── Log Info ──→│                │
 │              │               │   New User   │                │
 │              │               │               │←─ Log Saved ───│
 │              │               │               │                │
 │              │←─ Success Msg─│               │                │
 │              │   "Account    │               │                │
 │              │   Created"    │               │                │
 │              │               │               │                │
 │←─ Display ───│               │               │                │
 │  Success     │               │               │                │
 │  + Login Link│               │               │                │
 │              │               │               │                │
 ▼              ▼               ▼               ▼                ▼
```

---

## Sequence Diagram 4: View Forecast Flow

```
User         Browser        Flask App        WeatherAPI        Logger
 │              │               │               │                │
 │─ Click ─────→│               │               │                │
 │  View        │               │               │                │
 │  Forecast    │               │               │                │
 │              │               │               │                │
 │              │─ GET /forecast│               │                │
 │              │  ?city=London │               │                │
 │              │               │               │                │
 │              │               │─ Check──────→ │                │
 │              │               │  Session     │                │
 │              │               │  (Auth)      │                │
 │              │               │               │                │
 │              │               │─ Validate───→ │                │
 │              │               │  City Param  │                │
 │              │               │               │                │
 │              │               │──────────────→│ GET /forecast  │
 │              │               │  ?q=London    │ ?appid=KEY     │
 │              │               │               │                │
 │              │               │               │← 200 JSON ─────│
 │              │               │←──────────────│ (Forecast Data)│
 │              │               │               │                │
 │              │               │─ Extract Data│                │
 │              │               │  (5 days)    │                │
 │              │               │               │                │
 │              │               │─ Get City─────│                │
 │              │               │  Coordinates  │                │
 │              │               │  (from API)   │                │
 │              │               │               │                │
 │              │               │────────────────────────────→│
 │              │               │  Log Success                  │
 │              │               │  Forecast fetch             │
 │              │               │               │←─ Log OK ──────│
 │              │               │               │                │
 │              │               │─ Render Page─│                │
 │              │               │  (forecast.  │                │
 │              │               │   html)      │                │
 │              │               │               │                │
 │              │←─ Forecast Page│               │                │
 │              │  (5 cards,    │               │                │
 │              │   map)        │               │                │
 │              │               │               │                │
 │←─ Display ───│               │               │                │
 │  Forecast    │               │               │                │
 │  Page        │               │               │                │
 │              │               │               │                │
 ▼              ▼               ▼               ▼                ▼
```

---

## Sequence Diagram 5: Error Handling Flow

```
User         Browser        Flask App        Exception          Logger
 │              │               │             Handler            │
 │─ Search ─────│               │               │                │
 │  Invalid     │               │               │                │
 │  City        │               │               │                │
 │              │               │               │                │
 │              │─ POST /weather│               │                │
 │              │  ?city=XYZ123 │               │                │
 │              │               │               │                │
 │              │               │─ Validate───→ │                │
 │              │               │  Input       │                │
 │              │               │               │                │
 │              │               │─ Check──────X│                │
 │              │               │  Session     │ Fail            │
 │              │               │               │                │
 │              │               │─────────────────────→ Log Warn ─│
 │              │               │  Session Invalid              │
 │              │               │               │←─ Log OK ───────│
 │              │               │               │                │
 │              │               │─ Redirect───→ │                │
 │              │               │  to Login     │                │
 │              │               │               │                │
 │              │←─ 302 Redirect│               │                │
 │              │  /login       │               │                │
 │              │               │               │                │
 │←─ Go to ─────│               │               │                │
 │  Login Page  │               │               │                │
 │              │               │               │                │
 │              │               │─ Handle 302──→│                │
 │              │               │  Exception    │                │
 │              │               │               │                │
 │              │               │────────────────────────────→ Log │
 │              │               │               │               Info │
 │              │               │               │←─ Done ────────│
 │              │               │               │                │
 ▼              ▼               ▼               ▼                ▼
```

---

## Sequence Diagram 6: API Timeout Handling

```
User         Browser        Flask App        WeatherAPI        Logger
 │              │               │               │                │
 │─ Search ─────│               │               │                │
 │  London      │               │               │                │
 │              │               │               │                │
 │              │─ POST /weather│               │                │
 │              │  (London)     │               │                │
 │              │               │               │                │
 │              │               │─ Set Timeout─→│                │
 │              │               │  (10 seconds) │                │
 │              │               │               │                │
 │              │               │───────────────→│ GET request    │
 │              │               │                 │                │
 │              │               │   [waiting]    │                │
 │              │               │   [10 seconds] X API Server     │
 │              │               │   [timeout]     ✗ Down/Slow     │
 │              │               │                 │                │
 │              │               │←─ Timeout ─────│                │
 │              │               │  Exception     │                │
 │              │               │                 │                │
 │              │               │─ Catch Timeout→│                │
 │              │               │  Exception     │                │
 │              │               │                 │                │
 │              │               │────────────────────────────→ Log │
 │              │               │  Timeout Error                  │
 │              │               │                 │←─ Log OK ──────│
 │              │               │                 │                │
 │              │               │─ Show Error ──→│                │
 │              │               │  Page          │                │
 │              │               │                 │                │
 │              │←─ Error Page──│                 │                │
 │              │  (timeout    │                 │                │
 │              │   message)   │                 │                │
 │              │               │                 │                │
 │←─ Display ───│               │                 │                │
 │  Error       │               │                 │                │
 │  Message     │               │                 │                │
 │              │               │                 │                │
 ▼              ▼               ▼                 ▼                ▼
```

---

## Sequence Diagram 7: Complete User Session

```
User         Browser         Flask App        Services          Logger
 │              │               │               │                │
 │─ Visit ──────│               │               │                │
 │  App URL     │               │               │                │
 │              │               │               │                │
 │              │─ GET / ──────→│               │                │
 │              │               │               │                │
 │              │               │─ Check Session
 │              │               │  (no session) │                │
 │              │               │               │                │
 │              │←─ 302 to ─────│               │                │
 │              │  /login       │               │                │
 │              │               │               │                │
 │─ Click ─────→│               │               │                │
 │  Sign Up     │               │               │                │
 │              │               │               │                │
 │              │─ GET /signup─→│               │                │
 │              │               │               │                │
 │              │←─ Form HTML ──│               │                │
 │              │               │               │                │
 │─ Fill Form──→│               │               │                │
 │              │               │               │                │
 │              │─ POST /signup─│               │                │
 │              │               │               │                │
 │              │               │─ UserService─→│                │
 │              │               │  .register()  │─ Log Signup ───→│
 │              │               │               │←─ Log OK ───────│
 │              │               │               │                │
 │              │←─ Success ────│               │                │
 │              │               │               │                │
 │─ Click ─────→│               │               │                │
 │  Login       │               │               │                │
 │              │               │               │                │
 │              │─ GET /login──→│               │                │
 │              │               │               │                │
 │              │←─ Form HTML ──│               │                │
 │              │               │               │                │
 │─ Fill & ────→│               │               │                │
 │  Submit      │               │               │                │
 │              │─ POST /login──│               │                │
 │              │  (credentials)│               │                │
 │              │               │               │                │
 │              │               │─ UserService─→│                │
 │              │               │  .authenticate│─ Log Login ────→│
 │              │               │               │←─ Log OK ───────│
 │              │               │               │                │
 │              │               │─ Create Session
 │              │               │               │                │
 │              │←─ 302 to ─────│               │                │
 │              │  /weather     │               │                │
 │              │               │               │                │
 │─ Enter ─────→│               │               │                │
 │  City        │               │               │                │
 │              │               │               │                │
 │              │─ POST /weather│               │                │
 │              │  (city)       │               │               │
 │              │               │               │                │
 │              │               │─ WeatherSvc──→│                │
 │              │               │  .fetch()     │─ Log Search ───→│
 │              │               │  .extract()   │←─ Log OK ───────│
 │              │               │               │                │
 │              │←─ Weather ────│               │                │
 │              │  Results      │               │                │
 │              │               │               │                │
 │─ Click ─────→│               │               │                │
 │  Forecast    │               │               │                │
 │              │               │               │                │
 │              │─ GET /forecast│               │                │
 │              │  (city)       │               │                │
 │              │               │               │                │
 │              │               │─ WeatherSvc──→│                │
 │              │               │  .fetch()     │─ Log Forecast ─→│
 │              │               │  .extract()   │←─ Log OK ───────│
 │              │               │               │                │
 │              │←─ Forecast ───│               │                │
 │              │  Results      │               │                │
 │              │               │               │                │
 │─ Click ─────→│               │               │                │
 │  Logout      │               │               │                │
 │              │               │               │                │
 │              │─ GET /logout─→│               │                │
 │              │               │               │                │
 │              │               │─ Clear Session│─ Log Logout ───→│
 │              │               │               │←─ Log OK ───────│
 │              │               │               │                │
 │              │←─ 302 to ─────│               │                │
 │              │  /login       │               │                │
 │              │               │               │                │
 ▼              ▼               ▼               ▼                ▼
```

---

## Interaction Patterns

### Synchronous Call
```
Caller → Callee
↑
└─ Wait for response
```

### Asynchronous Call
```
Caller ─→ Callee
(doesn't wait for response)
```

### Loop (alt)
```
[loop] ─→ For each item
        Process item
        Log result
[end loop]
```

### Condition (alt)
```
[alt] ─→ If condition
        Path A
[else]
        Path B
[end alt]
```

---

## Summary of Sequences

| Sequence | Actors | Key Steps | Result |
|----------|--------|-----------|--------|
| Login | User, Browser, App, Service | Validate → Load → Verify → Create Session | User authenticated |
| Weather Search | User, Browser, App, API | Validate → Fetch → Extract → Display | Weather shown |
| Sign Up | User, Browser, App, Service | Validate → Check → Save → Log | Account created |
| Forecast | User, Browser, App, API | Authenticate → Fetch → Extract → Display | Forecast shown |
| Error | User, Browser, App, Handler | Try → Catch → Log → Render | Error displayed |
| Timeout | User, Browser, App, API | Request → Wait → Timeout → Handle | Error shown |
| Session | User, Browser, App, Services | Signup → Login → Use → Logout | Session ended |

---

## Message Types

- **Synchronous** (solid arrow): Caller waits for response
- **Asynchronous** (open arrow): Caller doesn't wait
- **Return** (dashed arrow): Response message
- **Create** (solid line with circle): Create new object
- **Destroy** (X mark): Destroy object
- **Activation Box**: Duration of method execution

---

## Timing Considerations

| Operation | Expected Time | Timeout |
|-----------|---|---|
| Input Validation | < 100ms | N/A |
| Database Read | < 50ms | N/A |
| API Call | < 3s | 10s |
| Page Render | < 500ms | N/A |
| Full Request | < 5s | N/A |

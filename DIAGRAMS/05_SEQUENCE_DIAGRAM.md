# Sequence Diagram - Weather App (Modular Architecture)

## Overview
Sequence diagrams show interactions between objects over time with the new modular architecture (UserService, WeatherService, models).

---

## Sequence Diagram 1: User Registration Flow

```
User          Browser         Flask (app.py)    UserService      File I/O      Logger
 │              │                  │                │              │              │
 │─ Click Signup→│                  │                │              │              │
 │              │                  │                │              │              │
 │              │                  │                │              │              │
 │←─ signup.html─│                  │                │              │              │
 │              │                  │                │              │              │
 │─ Fill Form──→│                  │                │              │              │
 │  (POST)      │                  │                │              │              │
 │              │─ POST /signup──→  │                │              │              │
 │              │   {email,         │                │              │              │
 │              │    username,      │                │              │              │
 │              │    password}      │                │              │              │
 │              │                  │                │              │              │
 │              │                  │─ register_user()→              │              │
 │              │                  │   (email, username, pwd)       │              │
 │              │                  │                │              │              │
 │              │                  │                ├─ Load users──→│              │
 │              │                  │                │  from file    │              │
 │              │                  │                │←─ User data───│              │
 │              │                  │                │              │              │
 │              │                  │                ├─ Validate    │              │
 │              │                  │                │  email       │              │
 │              │                  │                │  unique?     │              │
 │              │                  │                │              │              │
 │              │                  │                ├─ Create User │              │
 │              │                  │                │  object      │              │
 │              │                  │                │              │              │
 │              │                  │                ├─ Hash pwd    │              │
 │              │                  │                │              │              │
 │              │                  │                ├─ Save users──→│              │
 │              │                  │                │  to file      │              │
 │              │                  │                │←─ Success────│              │
 │              │                  │                │              │              │
 │              │                  │                ├─ Log────────────────────→   │
 │              │                  │                │  "User registered"         │
 │              │                  │                │              │              │
 │              │                  │←─ Return True─  │              │              │
 │              │                  │                │              │              │
 │              │←─ Redirect to Login────────────────────────────────────────────→│
 │              │                  │                │              │              │
 │←─ success msg─│                  │                │              │              │
 │              │                  │                │              │              │
 ▼              ▼                  ▼                ▼              ▼              ▼
```

---

## Sequence Diagram 2: User Login Flow

```
User          Browser         Flask (app.py)    UserService       Logger
 │              │                  │                │              │
 │─ Click Login→│                  │                │              │
 │              │                  │                │              │
 │←─ login.html─│                  │                │              │
 │              │                  │                │              │
 │─ Enter Email→│                  │                │              │
 │ & Password   │                  │                │              │
 │              │─ POST /login────→│                │              │
 │              │   (email, pwd)   │                │              │
 │              │                  │                │              │
 │              │                  │─ authenticate_user()→          │
 │              │                  │   (email, password)            │
 │              │                  │                │              │
 │              │                  │                ├─ Load users  │
 │              │                  │                │  from file   │
 │              │                  │                │              │
 │              │                  │                ├─ Find user   │
 │              │                  │                │  by email    │
 │              │                  │                │              │
 │              │                  │                ├─ Verify pwd  │
 │              │                  │                │  match       │
 │              │                  │                │              │
 │              │                  │                ├─ Create User │
 │              │                  │                │  object      │
 │              │                  │                │              │
 │              │                  │                ├─ Log────────→│
 │              │                  │                │  "Login OK"   │
 │              │                  │                │              │
 │              │                  │←─ Return User──│              │
 │              │                  │                │              │
 │              │                  ├─ Set Session  │              │
 │              │                  │  (user_email,  │              │
 │              │                  │   username)    │              │
 │              │                  │                │              │
 │              │                  ├─ Create       │              │
 │              │                  │  Session obj   │              │
 │              │                  │                │              │
 │              │←─ 302 Redirect───────────────────────────────────→│
 │              │  /weather        │                │              │
 │              │                  │                │              │
 │←─ Redirect──┤ │                  │                │              │
 │             │                  │                │              │
 ▼             ▼                  ▼                ▼              ▼
```

---

## Sequence Diagram 3: Weather Search Flow

```
User         Browser       Flask App      WeatherService    OpenWeather API    Logger
 │              │              │               │                  │              │
 │─ Search ────→│              │               │                  │              │
 │  City: London│              │               │                  │              │
 │              │              │               │                  │              │
 │              │─ POST /────→ │               │                  │              │
 │              │  weather    │               │                  │              │
 │              │  (city)     │               │                  │              │
 │              │              │               │                  │              │
 │              │              ├─ Check       │                  │              │
 │              │              │  Session     │                  │              │
 │              │              │  (auth OK)   │                  │              │
 │              │              │               │                  │              │
 │              │              ├─ get_current_weather("London")─→ │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Validate input  │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Make HTTP GET──→│              │
 │              │              │               │  /data/2.5/      │              │
 │              │              │               │  weather?q=...   │              │
 │              │              │               │                  │              │
 │              │              │               │←─ 200 OK (JSON)──│              │
 │              │              │               │  {temp, humidity │              │
 │              │              │               │   wind_speed, ...│
 │              │              │               │                  │              │
 │              │              │               ├─ Parse JSON      │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Create          │              │
 │              │              │               │  WeatherData obj │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Calculate wind  │              │
 │              │              │               │  direction       │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Log──────────→  │              │
 │              │              │               │  "Weather fetched│              │
 │              │              │               │                  │              │
 │              │              │←─ Return WeatherData object ──────│              │
 │              │              │               │                  │              │
 │              │              ├─ get_forecast("London")────→     │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Make HTTP GET──→│              │
 │              │              │               │  /data/2.5/      │              │
 │              │              │               │  forecast?q=...  │              │
 │              │              │               │                  │              │
 │              │              │               │←─ 200 OK (JSON)──│              │
 │              │              │               │  {list: [{...},  │              │
 │              │              │               │         ...]}    │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Parse JSON      │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Extract 5 days  │              │
 │              │              │               │                  │              │
 │              │              │               ├─ Create          │              │
 │              │              │               │  ForecastDay objs│              │
 │              │              │               │                  │              │
 │              │              │               ├─ Log──────────→  │              │
 │              │              │               │  "Forecast OK"   │              │
 │              │              │               │                  │              │
 │              │              │←─ Return List[ForecastDay]───────│              │
 │              │              │               │                  │              │
 │              │              ├─ Render       │                  │              │
 │              │              │  result.html  │                  │              │
 │              │              │  with data    │                  │              │
 │              │              │               │                  │              │
 │              │←─ HTML Page──│               │                  │              │
 │              │ with weather │               │                  │              │
 │              │ & forecast   │               │                  │              │
 │              │              │               │                  │              │
 │←─ Display ───┤              │               │                  │              │
 │  Results    │              │               │                  │              │
 │              │              │               │                  │              │
 ▼              ▼              ▼               ▼                  ▼              ▼
```

---

## Sequence Diagram 4: Error Handling Flow

```
User         Browser       Flask App      WeatherService       Logger
 │              │              │               │                 │
 │─ Search ────→│              │               │                 │
 │  Invalid City│              │               │                 │
 │              │              │               │                 │
 │              │─ POST /────→ │               │                 │
 │              │  weather    │               │                 │
 │              │  (invalid)  │               │                 │
 │              │              │               │                 │
 │              │              ├─ Check       │                 │
 │              │              │  Session     │                 │
 │              │              │  (auth OK)   │                 │
 │              │              │               │                 │
 │              │              ├─ get_current_weather()─→        │
 │              │              │               │                 │
 │              │              │               ├─ Validate       │
 │              │              │               │  input fails    │
 │              │              │               │                 │
 │              │              │               ├─ Log──────────→ │
 │              │              │               │  WARNING:       │
 │              │              │               │  Invalid input  │
 │              │              │               │                 │
 │              │              │               ├─ Exception:     │
 │              │              │               │  ValueError     │
 │              │              │               │                 │
 │              │              │←─ Return None──                │
 │              │              │               │                 │
 │              │              ├─ Check for    │                 │
 │              │              │  None result  │                 │
 │              │              │               │                 │
 │              │              ├─ Log────────────────────→       │
 │              │              │  ERROR: City not found          │
 │              │              │                 │               │
 │              │              ├─ Render       │                 │
 │              │              │  error.html   │                 │
 │              │              │  with message │                 │
 │              │              │               │                 │
 │              │←─ Error Page─│               │                 │
 │              │ (HTML 400)   │               │                 │
 │              │              │               │                 │
 │←─ Display ───┤              │               │                 │
 │  Error Msg  │              │               │                 │
 │              │              │               │                 │
 ▼              ▼              ▼               ▼                 ▼
```

---

## Sequence Diagram 5: Logout Flow

```
User         Browser       Flask App      UserService         Logger
 │              │              │               │                 │
 │─ Click ─────→│              │               │                 │
 │  Logout      │              │               │                 │
 │              │              │               │                 │
 │              │─ GET /──────→│               │                 │
 │              │  logout      │               │                 │
 │              │              │               │                 │
 │              │              ├─ Check       │                 │
 │              │              │  Session     │                 │
 │              │              │  (exists)    │                 │
 │              │              │               │                 │
 │              │              ├─ Get user    │                 │
 │              │              │  email from  │                 │
 │              │              │  session     │                 │
 │              │              │               │                 │
 │              │              ├─ Log────────────────────→       │
 │              │              │  INFO:                          │
 │              │              │  User logged out                │
 │              │              │               │                 │
 │              │              ├─ Clear       │                 │
 │              │              │  Session     │                 │
 │              │              │               │                 │
 │              │              ├─ Redirect    │                 │
 │              │              │  /login      │                 │
 │              │              │               │                 │
 │              │←─ 302 Redir──│               │                 │
 │              │  /login      │               │                 │
 │              │              │               │                 │
 │←─ Redirect──┤ │              │               │                 │
 │ to Login    │              │               │                 │
 │              │              │               │                 │
 ▼              ▼              ▼               ▼                 ▼
```
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

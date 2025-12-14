# Exception Handling & Logging Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEATHER APP - EXCEPTION HANDLING              │
└─────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │  User Input  │
                              └──────┬───────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                                  │
            ┌───────▼────────┐            ┌──────────▼─────────┐
            │   Validation   │            │   Route Handler    │
            │   Try-Catch    │            │   Try-Catch        │
            └───────┬────────┘            └──────────┬─────────┘
                    │                                 │
        ┌───────────▼──────────┐          ┌──────────▼──────────┐
        │ Input Sanitization   │          │ API Request         │
        │ Strip whitespace     │          │ Timeout: 10s        │
        │ Length validation    │          │                     │
        └───────────┬──────────┘          └──────────┬──────────┘
                    │                                 │
        ┌───────────▼──────────────────────┬─────────▼──────────┐
        │                                  │                     │
   ┌────▼─────┐                   ┌────────▼────────┐   ┌────────▼────────┐
   │ Timeout  │                   │ HTTP Error      │   │ Request Error   │
   │ Handlers │                   │ Handlers        │   │ Handlers        │
   └────┬─────┘                   └────────┬────────┘   └────────┬────────┘
        │                                  │                     │
        └──────────────────┬───────────────┴─────────────────────┘
                           │
                ┌──────────▼──────────┐
                │  Logger Instance    │
                │  (app_logger.py)    │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐    ┌─────▼──────┐
   │ File    │      │ Console     │    │ Log Level  │
   │ Handler │      │ Handler     │    │ Filter     │
   │ (DEBUG) │      │ (WARNING+)  │    │            │
   └────┬────┘      └──────┬──────┘    └─────┬──────┘
        │                  │                  │
   ┌────▼─────────────────┬┴─────────────────▼───┐
   │     logs/weather_app_YYYYMMDD.log            │
   │  (5MB rotation, 5 backups)                   │
   └──────────────────────────────────────────────┘
        │                  │
   ┌────▼─────────┐   ┌────▼──────────┐
   │  File Output │   │ Console Stream │
   │ Detailed log │   │ Short format   │
   └──────────────┘   └────────────────┘
```

---

## Error Handling Flow

```
REQUEST RECEIVED
      │
      ▼
┌─────────────────────┐
│ Flask Route Handler │
└────────┬────────────┘
         │
    ┌────▼────┐
    │ TRY     │
    └────┬────┘
         │
    ┌────▼─────────────────────────────────┐
    │ Business Logic (API calls, DB ops)   │
    │ - Validate inputs                    │
    │ - Make API requests                  │
    │ - Process data                       │
    └────┬──────────────┬────────┬─────────┘
         │              │        │
    SUCCESS        EXPECTED      UNEXPECTED
         │          ERROR         ERROR
         │              │             │
    ┌────▼─┐        ┌───▼────┐   ┌───▼─────────┐
    │ Log: │        │ Log:   │   │ Log:        │
    │ INFO │        │ ERROR  │   │ CRITICAL    │
    └────┬─┘        └───┬────┘   └───┬─────────┘
         │              │             │
    ┌────▼──┐       ┌───▼──────┐ ┌───▼──────────┐
    │Return │       │Render    │ │Render        │
    │Result │       │Error Page│ │Generic Error │
    └───┬───┘       └───┬──────┘ └───┬──────────┘
        │               │            │
        └───┬───────────┴────────────┘
            │
            ▼
      RESPONSE SENT
```

---

## Logging Levels & Usage

```
┌─────────────────────────────────────────────────────────────┐
│                      LOG LEVEL HIERARCHY                    │
└─────────────────────────────────────────────────────────────┘

DEBUG (10)      ▲
├─ API request details
├─ Data processing steps     ◄─── File Handler logs ALL
├─ Wind direction conversion  (logs/weather_app_*.log)
└─ Function call flow

INFO (20)       ◄─── Most Useful
├─ User login success
├─ User signup success       ◄─── Console shows this
├─ Weather data fetched       (WARNING level and above)
└─ Forecast processed

WARNING (30)    ◄─── Warning
├─ Invalid login attempt
├─ Weak password
├─ Missing optional fields
└─ Timeout occurred

ERROR (40)      ◄─── Error
├─ API failure
├─ File I/O error
├─ JSON parse error
├─ City not found
└─ Data extraction error

CRITICAL (50)   ◄─── System Critical
├─ App startup failure
└─ Unhandled exception
```

---

## Exception Type Handling Chain

```
REQUEST TRIGGERS EXCEPTION
         │
         ▼
    ┌─────────────────┐
    │ FIRST HANDLER   │
    │ Try-Except Block│      ┌─────────────────────────────┐
    └────┬────────────┘      │ Specific Exception Handling │
         │                   │ (Catch most specific first) │
    ┌────▼────────────────┐  └─────────────────────────────┘
    │ Type Check:         │
    │ ├─ KeyError?        │──→ Missing JSON field
    │ ├─ Timeout?         │──→ API request timeout
    │ ├─ HTTPError?       │──→ API HTTP error
    │ ├─ IOError?         │──→ File operation error
    │ ├─ ValueError?      │──→ Data validation error
    │ ├─ JSONError?       │──→ JSON decode error
    │ └─ Exception?       │──→ Generic fallback
    └────┬────────────────┘
         │
         ▼
    ┌──────────────────┐
    │ Specific Handler │
    │ - Log error      │
    │ - Return result  │
    │ - Continue app   │
    └──────────────────┘
```

---

## Request Flow with Error Handling

### Successful Request Path
```
User Request
    │
    ▼
Input Validation ✓
    │
    ▼
Database/API Call ✓
    │
    ▼
Data Processing ✓
    │
    ▼
logger.info("Success")
    │
    ▼
Return Result
    │
    ▼
User sees data ✓
```

### Error Request Path
```
User Request
    │
    ▼
Input Validation ✗ (Empty email)
    │
    ▼
logger.warning("Missing email field")
    │
    ▼
Return Error Message
    │
    ▼
User sees error ✗ (Nice message)
    │
    ▼
App continues running ✓
```

### Critical Error Path
```
User Request
    │
    ▼
Database Operation ✗ (File corruption)
    │
    ▼
except Exception caught
    │
    ▼
logger.critical("Database error")
    │
    ▼
Error Template Rendered
    │
    ▼
User sees error page ✗
    │
    ▼
App continues running ✓
```

---

## Logger Configuration

```
┌──────────────────────────────────────────────────────┐
│         utils/app_logger.py Configuration           │
└──────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Logger Instance: 'WeatherApp'                       │
│ Level: DEBUG (shows everything)                     │
└─────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                                  │
        ▼                                  ▼
┌──────────────────┐            ┌──────────────────┐
│ File Handler     │            │ Console Handler  │
│ RotatingFile     │            │ StreamHandler    │
├──────────────────┤            ├──────────────────┤
│ Level: DEBUG     │            │ Level: WARNING   │
│ Format: Detailed │            │ Format: Simple   │
│ Max Size: 5MB    │            │ Output: Console  │
│ Backup Count: 5  │            │                  │
└──────────────────┘            └──────────────────┘
        │                                  │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────┼───────────────────┐
        │                │                   │
        ▼                ▼                   ▼
    logs/          Console Output      Log Analysis
    weather_app    (Warnings+)         (Files Only)
    YYYYMMDD.log
```

---

## Error Page Flow

```
Exception Occurs
    │
    ▼
@app.errorhandler catches it
    │
    ├─────────────────────────────┐
    │                              │
404 Handler           500 Handler   Generic Handler
    │                      │            │
    ▼                      ▼            ▼
log.warning()         log.critical()  log.critical()
    │                      │            │
    ▼                      ▼            ▼
render_template('error.html')
    │
    ▼
Pass: error_code, error_message
    │
    ▼
error.html displays:
├─ Large error code (404/500)
├─ Clear message
├─ Helpful suggestions
└─ Navigation buttons
    │
    ▼
User can:
├─ Go to Home
└─ Go Back
```

---

## Production Ready Checklist

```
✅ Exception Handling
   ├─ All routes protected with try-except
   ├─ Specific exception types caught
   ├─ Graceful error recovery
   └─ User-friendly messages

✅ Logging System
   ├─ Multi-level logging (DEBUG-CRITICAL)
   ├─ File and console handlers
   ├─ Log rotation implemented
   └─ Detailed context in logs

✅ Error Handling
   ├─ Global error handlers (400, 404, 500)
   ├─ Unhandled exception handler
   ├─ Error template rendering
   └─ Navigation recovery

✅ Input Validation
   ├─ Empty field checks
   ├─ Type validation
   ├─ Length validation
   └─ Whitespace sanitization

✅ API Resilience
   ├─ Timeout protection (10s)
   ├─ HTTP error handling
   ├─ Network error handling
   └─ JSON parsing errors

✅ Monitoring
   ├─ User action tracking
   ├─ Error frequency tracking
   ├─ Performance monitoring
   └─ Audit trail creation
```

---

## Statistics & Monitoring

```
Logs Available For:
├─ User Authentication (who logged in/out)
├─ API Calls (what data was fetched)
├─ Errors (what went wrong)
├─ Warnings (potential issues)
└─ Debug Info (detailed flow tracking)

Analysis Commands:
├─ grep "ERROR" logs/* (find all errors)
├─ grep "user@" logs/* (track user activity)
├─ tail -f logs/* (real-time monitoring)
├─ wc -l logs/* (log size tracking)
└─ grep "timeout" logs/* (performance issues)
```

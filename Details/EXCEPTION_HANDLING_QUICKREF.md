# Exception Handling & Logging - Quick Reference

## What Was Added

### 1. **New Logger Module** (`utils/app_logger.py`)
- Centralized logging configuration
- File handler: detailed logs with rotation
- Console handler: warnings and errors only
- Automatic log directory creation

### 2. **Exception Handling**
Added try-except blocks to all critical functions:
- User authentication (login/signup)
- File operations (load/save users)
- API requests (weather/forecast)
- Data extraction (weather/forecast processing)
- Route handlers

### 3. **Error Handlers**
Global Flask error handlers for:
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error
- Unhandled Exceptions

### 4. **Error Template** (`templates/error.html`)
User-friendly error pages with helpful information

### 5. **Documentation** (`LOGGING_DOCUMENTATION.md`)
Comprehensive guide on the logging system

---

## Key Features

### Logging Points
✅ Application startup/shutdown
✅ User authentication (login, signup, logout)
✅ Weather searches and API calls
✅ Data processing and extraction
✅ Errors and exceptions
✅ User actions and events

### Exception Types Handled
✅ File I/O errors
✅ JSON decoding errors
✅ API timeout errors
✅ HTTP errors
✅ Network errors
✅ Data validation errors
✅ Unhandled exceptions

### Log Levels
```
DEBUG   → Detailed diagnostic info
INFO    → General operations
WARNING → Recoverable issues
ERROR   → Operation failures
CRITICAL → System failures
```

---

## Using the Logger

### Import
```python
from utils.app_logger import logger
```

### Basic Usage
```python
logger.debug("Detailed message")
logger.info("Operation successful")
logger.warning("Something unexpected")
logger.error("An error occurred")
logger.critical("Critical failure")
```

### With Context
```python
logger.info(f"Successful login for user: {email}")
logger.error(f"Timeout fetching weather for {city}: {error}")
logger.warning(f"Missing optional field: {field_name}")
```

---

## Log Files

### Location
```
Weather_App_Project/logs/weather_app_YYYYMMDD.log
```

### View Logs
```bash
# View real-time logs
tail -f logs/weather_app_*.log

# View errors only
grep "ERROR" logs/weather_app_*.log

# View specific date
tail -100 logs/weather_app_20231214.log
```

---

## Exception Handling Pattern

```python
try:
    # Operation that might fail
    result = risky_operation()
    logger.info("Operation completed")
    return result

except SpecificError as e:
    logger.error(f"Specific error: {e}")
    return error_response()

except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return fallback_response()
```

---

## Testing

### All modules compile without errors ✅
```bash
python -m py_compile app.py
python -m py_compile utils/app_logger.py
```

### Log files will be created automatically when app runs:
```
logs/
└── weather_app_20231214.log
```

### Console will show warnings and errors:
```
2025-12-14 14:32:15 - WARNING - Login attempt with missing fields
2025-12-14 14:33:10 - ERROR - Timeout fetching weather for London
```

---

## Production Ready Features

✅ **Graceful Error Handling** - App doesn't crash on errors
✅ **Comprehensive Logging** - Track everything that happens
✅ **User-Friendly Errors** - Non-technical error messages
✅ **Log Rotation** - Automatic cleanup of old logs
✅ **Multiple Log Levels** - DEBUG to CRITICAL logging
✅ **Timeouts** - 10-second timeout on API requests
✅ **Input Validation** - Sanitize and validate all inputs
✅ **Fallback Values** - Gracefully degrade functionality
✅ **Detailed Error Pages** - Help users recover from errors
✅ **Audit Trail** - Track all user actions

---

## Next Steps

1. **Run the app**: `python app.py`
2. **Check logs**: Look in `logs/` directory for logs
3. **Monitor errors**: Check console for WARNING and ERROR level logs
4. **Test error scenarios**: Try invalid cities, bad inputs, etc.
5. **Review logs**: Use `tail -f` to monitor in real-time

---

## Files Modified/Created

### Modified Files
- ✏️ `app.py` - Added exception handling and logging
- ✏️ `utils/logger.py` - Updated with comments

### New Files
- ✨ `utils/app_logger.py` - New logger configuration
- ✨ `templates/error.html` - Error page template
- ✨ `LOGGING_DOCUMENTATION.md` - Complete documentation
- ✨ `EXCEPTION_HANDLING_QUICKREF.md` - This file

# Weather App - Exception Handling & Logging Documentation

## Overview
The Weather App now includes comprehensive exception handling and logging throughout the application. This ensures robust error management, detailed debugging information, and production-ready monitoring.

---

## Logging System

### Logger Configuration (`utils/app_logger.py`)
The centralized logging system is configured with:

#### Log Levels
- **DEBUG**: Detailed diagnostic information (API calls, data processing)
- **INFO**: General informational messages (successful operations, user actions)
- **WARNING**: Warning messages (unverified inputs, missing optional data)
- **ERROR**: Error messages (API failures, data processing errors)
- **CRITICAL**: Critical errors (application startup failures)

#### Log Output
1. **File Handler**
   - Location: `logs/weather_app_YYYYMMDD.log`
   - Level: DEBUG (logs everything)
   - Format: `%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s`
   - Rotation: 5MB max file size with 5 backup files

2. **Console Handler**
   - Level: WARNING and above
   - Format: `%(asctime)s - %(levelname)s - %(message)s`
   - Displays only important messages in terminal

### Usage in Code
```python
from utils.app_logger import logger

logger.debug("Detailed diagnostic message")
logger.info("Operation completed successfully")
logger.warning("Something unexpected happened")
logger.error("An error occurred")
logger.critical("Critical failure")
```

---

## Exception Handling Patterns

### 1. **File Operations** (load_users, save_users)
```python
try:
    with open(USERS_FILE, 'r') as f:
        return json.load(f)
except json.JSONDecodeError as e:
    logger.error(f"Error decoding JSON: {e}")
    return {}
except IOError as e:
    logger.error(f"IO Error: {e}")
    return {}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {}
```

**Handles:**
- JSON decoding errors
- File I/O errors
- Unexpected exceptions
- Graceful fallback with empty dict

### 2. **API Requests**
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    logger.error("Request timeout")
except requests.exceptions.HTTPError as e:
    logger.error(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    logger.error(f"Request error: {e}")
```

**Handles:**
- Request timeouts (10 second timeout set)
- HTTP errors (4xx, 5xx status codes)
- Network errors
- JSON parsing errors

### 3. **Data Validation**
```python
try:
    if not all([username, email, password]):
        logger.warning("Missing required fields")
        return error_response
    
    if password != confirm_password:
        logger.warning("Passwords don't match")
        return error_response
except Exception as e:
    logger.error(f"Validation error: {e}")
```

**Handles:**
- Empty/missing input validation
- Data consistency checks
- Password validation

### 4. **Route Error Handlers**
```python
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {request.url}")
    return render_template('error.html', error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    logger.critical(f"500 Internal Server Error: {error}")
    return render_template('error.html', error_code=500), 500
```

---

## Logged Events

### Authentication
- ✅ Successful logins
- ❌ Failed login attempts
- ✅ New user registrations
- 🚪 User logouts
- ⚠️ Invalid input during signup

### Weather Operations
- 📍 City search requests
- ✅ Successful weather data retrieval
- ❌ API timeout/failure
- 📊 Forecast data processing
- ⚠️ Missing optional weather fields

### Data Processing
- 📈 Weather data extraction
- 🧭 Wind direction conversion
- 🗓️ Forecast aggregation
- ⚠️ Missing fields (logged as warnings, not errors)

### System Events
- 🚀 Application startup
- 💥 Critical errors
- 🔄 Unexpected exceptions

---

## Log File Location
```
Weather_App_Project/
├── logs/
│   ├── weather_app_20231214.log
│   ├── weather_app_20231213.log
│   └── ...
```

### Log File Format
```
2025-12-14 14:32:15,123 - WeatherApp - INFO - [app.py:145] - Successful login for user: user@example.com
2025-12-14 14:32:45,456 - WeatherApp - DEBUG - [app.py:230] - Fetching weather data for city: London
2025-12-14 14:33:10,789 - WeatherApp - ERROR - [app.py:240] - Request timeout while fetching weather for London
```

---

## Error Pages

### Error Template (`templates/error.html`)
User-friendly error pages for:
- **400 Bad Request** - Invalid input
- **404 Not Found** - Page not found
- **500 Internal Server Error** - Server error

Features:
- Clear error messages
- Home button
- Back button
- Helpful suggestions

---

## Best Practices

### When Adding New Code
1. **Always use try-except for**:
   - File operations
   - API requests
   - Data parsing (JSON, datetime)
   - Database operations
   - User input validation

2. **Logging guidelines**:
   - Use DEBUG for detailed flow (API calls, data processing)
   - Use INFO for major operations (login, search, data fetch)
   - Use WARNING for recoverable issues
   - Use ERROR for failures that affect functionality
   - Use CRITICAL only for system failures

3. **Error handling strategy**:
   - Catch specific exceptions first
   - Log with enough context (user ID, city name, etc.)
   - Provide user-friendly error messages
   - Gracefully degrade functionality when possible

### Example Pattern
```python
try:
    # Operation that might fail
    result = perform_operation(data)
    logger.info(f"Operation successful for {identifier}")
    return result
except SpecificException as e:
    logger.error(f"Specific error for {identifier}: {e}")
    return error_response()
except Exception as e:
    logger.error(f"Unexpected error for {identifier}: {e}")
    return generic_error_response()
```

---

## Viewing Logs

### Real-time Logs (Terminal)
The console handler shows WARNING level and above:
```bash
2025-12-14 14:32:15 - WARNING - Login attempt with missing email or password
2025-12-14 14:33:10 - ERROR - Request timeout while fetching weather
```

### Complete Logs (File)
Check the logs directory for detailed DEBUG-level logs:
```bash
cat logs/weather_app_20231214.log
tail -f logs/weather_app_20231214.log  # Real-time tail
```

### Log Analysis
```bash
# View all errors
grep "ERROR" logs/weather_app_*.log

# View specific user activity
grep "user@example.com" logs/weather_app_*.log

# View API errors
grep "request error\|timeout" logs/weather_app_*.log

# Count errors by type
grep "ERROR" logs/weather_app_*.log | cut -d'-' -f4 | sort | uniq -c
```

---

## Configuration

### Changing Log Level
Edit `utils/app_logger.py`:
```python
self.logger.setLevel(logging.DEBUG)  # Change to INFO, WARNING, ERROR, CRITICAL
```

### Changing Log File Location
Edit `utils/app_logger.py`:
```python
self.log_dir = 'custom_logs_path'  # Default is 'logs'
```

### Changing Log Rotation Size
Edit `utils/app_logger.py`:
```python
file_handler = logging.handlers.RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # Changed to 10MB
    backupCount=10
)
```

---

## Troubleshooting

### No logs appearing?
1. Check `logs/` directory exists
2. Verify Flask debug mode is enabled
3. Check file permissions on logs directory

### Logs too verbose?
1. Increase log level in app_logger.py
2. Filter logs by level: `grep "ERROR\|WARNING" logs/*`

### Logs too detailed?
1. Decrease debug output by reducing DEBUG level logs
2. Use file filtering to view only specific categories

---

## Summary
The Weather App now has production-ready error handling and comprehensive logging that enables:
- ✅ Quick error diagnosis
- ✅ User activity tracking
- ✅ Performance monitoring
- ✅ Security audit trails
- ✅ Graceful error recovery

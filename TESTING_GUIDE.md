# Testing Exception Handling & Logging

## Quick Test Guide

### 1. Start the Application

```bash
cd Weather_App_Project
python app.py
```

Expected output:
```
==================================================
Weather App Starting
==================================================
 * Running on http://127.0.0.1:5000
```

A new log file should be created:
```
logs/weather_app_20231214.log
```

---

## Test Scenarios

### Test 1: Login with Missing Email
**What to do:**
1. Go to Login page
2. Leave Email empty, enter password
3. Click Login

**Expected results:**
- ❌ Error message: "Email and password are required!"
- 📝 Log entry: `WARNING - Login attempt with missing email or password`
- ✅ App continues running

**Check logs:**
```bash
grep "missing email\|password are required" logs/weather_app_*.log
```

---

### Test 2: Login with Invalid Credentials
**What to do:**
1. Enter invalid email/password combo
2. Click Login

**Expected results:**
- ❌ Error message: "Invalid email or password!"
- 📝 Log entry: `WARNING - Failed login attempt for email: invalid@example.com`
- ✅ App continues running

**Check logs:**
```bash
grep "Failed login" logs/weather_app_*.log
```

---

### Test 3: Successful Login
**What to do:**
1. Use valid credentials (create account first if needed)
2. Click Login

**Expected results:**
- ✅ Redirected to weather page
- 📝 Log entry: `INFO - Successful login for user: email@example.com`
- ✅ Session created

**Check logs:**
```bash
grep "Successful login" logs/weather_app_*.log
```

---

### Test 4: Weather Search with Invalid City
**What to do:**
1. Login successfully
2. Search for "InvalidCityXYZ123"
3. Click Search

**Expected results:**
- ❌ Error message: "City not found: InvalidCityXYZ123. Please enter a valid city name."
- 📝 Log entry: `WARNING - City not found: InvalidCityXYZ123`
- ✅ App continues running, can search again

**Check logs:**
```bash
grep "City not found" logs/weather_app_*.log
```

---

### Test 5: Weather Search with Valid City
**What to do:**
1. Login successfully
2. Search for "London"
3. Click Search

**Expected results:**
- ✅ Weather data displayed with map
- 📝 Log entries:
  - `INFO - Fetching weather data for city: London`
  - `INFO - Successfully fetched weather and forecast for London`
- ✅ Both current weather and forecast loaded

**Check logs:**
```bash
grep "Successfully fetched weather" logs/weather_app_*.log
```

---

### Test 6: Forecast Page Access
**What to do:**
1. From weather results, click "5-Day Forecast"
2. Verify forecast page loads

**Expected results:**
- ✅ 5-day forecast displayed
- 📝 Log entry: `INFO - Successfully fetched forecast for London, GB`
- ✅ Map shows correct location
- 📝 Coordinates displayed correctly

**Check logs:**
```bash
grep "Successfully fetched forecast" logs/weather_app_*.log
```

---

### Test 7: Invalid Input on Signup
**What to do:**
1. Go to Signup page
2. Leave some fields empty
3. Click Register

**Expected results:**
- ❌ Error message: "All fields are required!"
- 📝 Log entry: `WARNING - Signup attempt with missing fields`
- ✅ Can try again

**Check logs:**
```bash
grep "Signup attempt with missing\|weak password" logs/weather_app_*.log
```

---

### Test 8: Logout
**What to do:**
1. Login successfully
2. Click Logout

**Expected results:**
- ✅ Redirected to login page
- 📝 Log entry: `INFO - User user@example.com logging out`
- ✅ Session cleared

**Check logs:**
```bash
grep "logging out" logs/weather_app_*.log
```

---

### Test 9: Access Protected Page Without Login
**What to do:**
1. Logout (if logged in)
2. Try to access `/weather` directly (type in URL)

**Expected results:**
- ↔️ Redirected to login page
- 📝 Log entry: `WARNING - Unauthenticated user attempting to access weather page`
- ✅ Cannot access without login

**Check logs:**
```bash
grep "Unauthenticated" logs/weather_app_*.log
```

---

### Test 10: Check Log File Format
**What to do:**
1. Run any test above
2. Check the log file directly

**Expected results:**
```
2025-12-14 14:32:15,123 - WeatherApp - INFO - [app.py:150] - Successful login for user: user@example.com
                           ^                    ^                 ^
                         Logger Name         Level             Message with context
```

**View logs:**
```bash
tail -20 logs/weather_app_*.log
```

---

## Log Analysis Commands

### View All Errors
```bash
grep "ERROR" logs/weather_app_*.log
```

### View All Warnings
```bash
grep "WARNING" logs/weather_app_*.log
```

### View Login Activity
```bash
grep "login\|logout" logs/weather_app_*.log
```

### View API Calls
```bash
grep "Fetching\|Successfully fetched" logs/weather_app_*.log
```

### Real-Time Log Monitoring
```bash
tail -f logs/weather_app_*.log
```

### Count Log Levels
```bash
echo "INFO entries:" $(grep -c "INFO" logs/weather_app_*.log)
echo "WARNING entries:" $(grep -c "WARNING" logs/weather_app_*.log)
echo "ERROR entries:" $(grep -c "ERROR" logs/weather_app_*.log)
```

### Find Errors by Type
```bash
# API timeout errors
grep "timeout\|Timeout" logs/weather_app_*.log

# File errors
grep "IO Error\|File not found" logs/weather_app_*.log

# Validation errors
grep "Invalid\|required" logs/weather_app_*.log
```

---

## Expected Log Output Examples

### Successful User Journey
```
INFO - User user@example.com accessing home, redirecting to weather
INFO - Successful login for user: user@example.com
DEBUG - Login attempt for email: user@example.com
INFO - Fetching weather data for city: London
INFO - Successfully fetched weather and forecast for London
DEBUG - Converting 45 degrees to wind direction: NE
INFO - User user@example.com logging out
```

### Error Handling
```
WARNING - Login attempt with missing email or password
WARNING - Failed login attempt for email: wrong@example.com
WARNING - City not found: InvalidCity
DEBUG - Unexpected error in weather route for city London
ERROR - Request error fetching weather for Tokyo
WARNING - Unauthenticated user attempting to access weather page
```

---

## Performance Testing

### Check Log File Size
```bash
ls -lh logs/weather_app_*.log
```

### Monitor Log Growth
```bash
watch 'wc -l logs/weather_app_*.log'
```

### Find Slow Operations (look for timestamps)
```bash
# Shows timestamp differences
tail -100 logs/weather_app_*.log | head -2
tail -100 logs/weather_app_*.log | tail -1
```

---

## Troubleshooting

### No logs appearing?
1. Check if `logs/` directory exists
2. Check file permissions: `ls -la logs/`
3. Try creating a test log entry in Python:
   ```python
   from utils.app_logger import logger
   logger.info("Test message")
   ```

### Logs file is huge?
1. Check number of lines: `wc -l logs/weather_app_*.log`
2. Old logs are auto-rotated (5MB max)
3. Max 5 backup files kept

### Can't find specific log entry?
1. Check correct date: `ls logs/weather_app_*.log`
2. Use grep with case-insensitive: `grep -i "login" logs/weather_app_*.log`
3. Check for partial strings: `grep "log" logs/weather_app_*.log`

---

## Summary Checklist

After testing, verify:

- [ ] Logs directory created (`logs/`)
- [ ] Log file created (`weather_app_YYYYMMDD.log`)
- [ ] INFO entries for successful operations
- [ ] WARNING entries for validation issues
- [ ] ERROR entries for failures
- [ ] User login/logout tracked
- [ ] API calls logged
- [ ] Error pages display correctly
- [ ] App continues running after errors
- [ ] No unhandled exceptions in logs

---

## Production Monitoring

Once in production:

1. **Daily Log Review**
   ```bash
   grep "ERROR\|CRITICAL" logs/weather_app_*.log
   ```

2. **User Activity Audit**
   ```bash
   grep "login\|logout\|signup" logs/weather_app_*.log
   ```

3. **API Health Check**
   ```bash
   grep "timeout\|HTTP error" logs/weather_app_*.log
   ```

4. **Log Rotation Verification**
   ```bash
   ls -la logs/ | wc -l
   ```

---

## Common Test Cases

### Positive Test Cases (Should Succeed)
- ✅ Valid login
- ✅ Valid signup
- ✅ Search valid city
- ✅ View forecast
- ✅ Logout

### Negative Test Cases (Should Show Errors)
- ❌ Login with wrong password
- ❌ Signup with weak password
- ❌ Search invalid city
- ❌ Missing required fields
- ❌ Access protected pages without login

### Edge Cases (Should Handle Gracefully)
- ⚠️ Empty search field
- ⚠️ Whitespace in input
- ⚠️ Very long city names
- ⚠️ Special characters in search
- ⚠️ Network timeout simulation

All should result in user-friendly errors, not crashes! ✨

# Code Changes - Before & After Examples

## 1. API Response Code Handling

### ❌ BEFORE (Broken)
```python
# services.py - get_current_weather method
if data.get('cod') != 200:  # Only checks integer!
    logger.warning(f"City not found: {city}")
    return None
```

**Problem:** OpenWeather API returns `cod` as string `'200'`, not integer `200`

### ✅ AFTER (Fixed)
```python
# services.py - get_current_weather method
cod = data.get('cod')
if str(cod) != '200':  # Handles both string and integer
    logger.warning(f"City not found: {city}. API Response code: {cod}")
    return None

try:
    # Create WeatherData object
    weather = WeatherData(data)
    weather.wind_direction = self._get_wind_direction(weather.wind_deg)
except (KeyError, TypeError, ValueError) as e:
    logger.error(f"Error creating WeatherData object for {city}: {e}")
    return None
```

**Improvement:** Now handles both `cod: 200` and `cod: '200'`, plus catches creation errors

---

## 2. ForecastDay Object Creation

### ❌ BEFORE (Broken)
```python
# services.py - get_forecast method
# This list comprehension has variable shadowing problem!
result = [
    ForecastDay(date, data['day'], data)
    for date, data in list(daily_forecasts.items())[:5]
]
```

**Problem:** `data` variable is reused (shadows outer scope), making logic confusing

### ✅ AFTER (Fixed)
```python
# services.py - get_forecast method
# Explicit loop with clear variable names
result = []
for date_key in list(daily_forecasts.keys())[:5]:
    forecast_data = daily_forecasts[date_key]
    try:
        forecast_day = ForecastDay(date_key, forecast_data['day'], forecast_data)
        result.append(forecast_day)
    except Exception as e:
        logger.warning(f"Error creating ForecastDay object for {date_key}: {e}")
        continue
```

**Improvement:** Clear variable names, proper error handling, readable logic

---

## 3. WeatherData Initialization

### ❌ BEFORE (Fragile)
```python
# models.py - WeatherData.__init__
self.city = data.get('name')  # Could be None
self.country = data.get('sys', {}).get('country')  # Could be None
self.latitude = round(data.get('coord', {}).get('lat', 0), 4)

# This line crashes if timestamp is 0!
self.sunrise = datetime.fromtimestamp(
    data.get('sys', {}).get('sunrise', 0)
).strftime('%I:%M %p')

self.rain = round(data.get('rain', {}).get('1h', 0), 1)
```

**Problems:**
- No defaults for required fields
- Timestamp conversion crashes on 0 or invalid values
- No error handling for the entire initialization

### ✅ AFTER (Robust)
```python
# models.py - WeatherData.__init__
try:
    self.city = data.get('name', 'Unknown')  # Has default!
    self.country = data.get('sys', {}).get('country', 'N/A')  # Has default!
    self.latitude = round(data.get('coord', {}).get('lat', 0), 4)
    
    # Safe timestamp handling with fallback
    sys_data = data.get('sys', {})
    sunrise_ts = sys_data.get('sunrise', 0)
    sunset_ts = sys_data.get('sunset', 0)
    
    try:
        self.sunrise = (
            datetime.fromtimestamp(sunrise_ts).strftime('%I:%M %p') 
            if sunrise_ts else 'N/A'
        )
        self.sunset = (
            datetime.fromtimestamp(sunset_ts).strftime('%I:%M %p') 
            if sunset_ts else 'N/A'
        )
    except (OSError, ValueError) as e:
        self.sunrise = 'N/A'
        self.sunset = 'N/A'
    
    self.rain = round(data.get('rain', {}).get('1h', 0), 1)
    
except Exception as e:
    raise ValueError(f"Error initializing WeatherData: {e}")
```

**Improvements:**
- All fields have sensible defaults
- Timestamps handled safely
- Entire initialization wrapped in try-except
- Better error reporting

---

## 4. Forecast Data Processing

### ❌ BEFORE (Error-prone)
```python
# services.py - get_forecast method
forecast_list = data.get('list', [])
daily_forecasts = {}

for forecast in forecast_list:
    try:
        dt = datetime.fromtimestamp(forecast['dt'])
        date_key = dt.strftime('%Y-%m-%d')
        day_name = dt.strftime('%A')
        
        if date_key not in daily_forecasts:
            daily_forecasts[date_key] = {
                'date': date_key,
                'day': day_name,
                'temp_max': forecast['main']['temp_max'],  # Could crash!
                'temp_min': forecast['main']['temp_min'],  # Could crash!
                'temp': forecast['main']['temp'],
                'humidity': forecast['main']['humidity'],
                'description': forecast['weather'][0]['description'].title(),  # Could crash!
                'icon': forecast['weather'][0]['icon'],
                'wind_speed': forecast['wind']['speed'],  # Could crash!
                'rain_chance': forecast['pop'] * 100,  # Could crash!
            }
    except KeyError as e:
        logger.warning(f"Missing key in forecast item: {e}, skipping")
        continue
```

**Problems:**
- Direct dictionary access without .get()
- No validation that 'weather' or 'wind' exist
- `pop` might be missing
- No logic to aggregate daily data from multiple forecast entries

### ✅ AFTER (Safe)
```python
# services.py - get_forecast method
forecast_list = data.get('list', [])
if not forecast_list:
    logger.warning(f"No forecast data available for {city}")
    return None

daily_forecasts = {}

for forecast in forecast_list:
    try:
        dt = datetime.fromtimestamp(forecast['dt'])
        date_key = dt.strftime('%Y-%m-%d')
        day_name = dt.strftime('%A')
        
        if date_key not in daily_forecasts:
            daily_forecasts[date_key] = {
                'day': day_name,
                'temp_max': forecast['main'].get('temp_max', 0),  # Safe!
                'temp_min': forecast['main'].get('temp_min', 0),  # Safe!
                'temp': forecast['main'].get('temp', 0),
                'humidity': forecast['main'].get('humidity', 0),
                # Safe access to weather array
                'description': (
                    forecast['weather'][0].get('description', '').title() 
                    if forecast.get('weather') else 'N/A'
                ),
                'icon': (
                    forecast['weather'][0].get('icon', '') 
                    if forecast.get('weather') else ''
                ),
                # Safe access to wind
                'wind_speed': forecast['wind'].get('speed', 0),
                # Safe access to pop with calculation
                'rain_chance': round((forecast.get('pop', 0) * 100), 1),
            }
        else:
            # Aggregate daily data - update max/min
            if forecast['main'].get('temp_max', 0) > daily_forecasts[date_key]['temp_max']:
                daily_forecasts[date_key]['temp_max'] = forecast['main'].get('temp_max', 0)
            if forecast['main'].get('temp_min', 0) < daily_forecasts[date_key]['temp_min']:
                daily_forecasts[date_key]['temp_min'] = forecast['main'].get('temp_min', 0)
    except (KeyError, ValueError, TypeError) as e:
        logger.warning(f"Error processing forecast item: {e}, skipping")
        continue
```

**Improvements:**
- All dictionary access uses .get() with defaults
- Pre-checks for optional arrays like 'weather'
- Proper daily aggregation logic
- Better exception handling with specific types

---

## 5. Error Messages

### ❌ BEFORE (Unhelpful)
```python
# app.py - weather route
except Exception as e:
    logger.error(f"Unexpected error in weather route: {e}")
    return render_template('index.html', 
                         error="An error occurred while fetching weather data.",
                         username=session.get('username'))
```

**Problem:** Generic message doesn't help users understand what went wrong

### ✅ AFTER (Helpful)
```python
# app.py - weather route
except Exception as e:
    logger.error(f"Unexpected error in weather route: {e}", exc_info=True)
    return render_template('index.html', 
                         error=f"An error occurred: {str(e)}",
                         username=session.get('username'))

# Also for weather not found
if not weather_data:
    logger.warning(f"City not found or API error: {city}")
    error = f"City '{city}' not found. Please check the spelling and try again."
    return render_template('index.html', error=error, 
                         username=session.get('username'))
```

**Improvements:**
- Users see actual error message
- Stack trace logged with exc_info=True
- Specific helpful messages (e.g., "check the spelling")

---

## Summary of Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **API Code Check** | Integer only | String or Integer |
| **Data Access** | Direct access | .get() with defaults |
| **Error Handling** | Basic | Comprehensive |
| **Logging** | Generic | Detailed & Useful |
| **Code Clarity** | List comprehension | Explicit loop |
| **Edge Cases** | Ignored | Handled |
| **User Messages** | Generic | Specific & Helpful |

---

## Key Takeaways

1. **Always use `.get()` for optional data**
2. **Handle external API responses defensively**
3. **Provide meaningful error messages to users**
4. **Log detailed information for debugging**
5. **Test edge cases and error scenarios**
6. **Validate data before processing**


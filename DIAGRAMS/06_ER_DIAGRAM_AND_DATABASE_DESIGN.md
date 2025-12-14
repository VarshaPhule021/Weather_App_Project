# ER Diagram & Database Design - Weather App (Modular Architecture)

## Overview
The Entity-Relationship (ER) diagram shows the data structures and relationships in the Weather App with the new modular architecture.

---

## ER Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│                      USERS TABLE                                │
├─────────────────────────────────────────────────────────────────┤
│ email           (str, PK)      - User's email address           │
│ username        (str)          - User's display name            │
│ password        (str)          - Hashed password (bcrypt)       │
│ created_at      (datetime)     - Account creation timestamp     │
├─────────────────────────────────────────────────────────────────┤
│ Relationships:                                                  │
│ - One User can have one active Session (1:1)                   │
│ - User data persisted in users.json file                        │
└──────────────┬──────────────────────────────────────────────────┘
               │
               │ 1:1 Relationship (active session)
               │
┌──────────────▼──────────────────────────────────────────────────┐
│                    SESSIONS TABLE                               │
├─────────────────────────────────────────────────────────────────┤
│ user_email      (str, FK)      - Reference to Users.email       │
│ username        (str)          - Denormalized from User         │
│ created_at      (datetime)     - Session creation time          │
│ last_activity   (datetime)     - Last user activity time        │
├─────────────────────────────────────────────────────────────────┤
│ Relationships:                                                  │
│ - Many Sessions per User (current: 1, but design allows >1)    │
│ - Sessions stored in Flask session (cookies/server-side)       │
└──────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                  WEATHER_DATA (In-Memory)                       │
├─────────────────────────────────────────────────────────────────┤
│ Attributes (all from OpenWeather API response):                │
├─────────────────────────────────────────────────────────────────┤
│ Location Information:                                           │
│ ├─ city               (str)          - City name                │
│ ├─ country            (str)          - Country code (2-letter)  │
│ ├─ latitude           (float)        - Geographic latitude      │
│ └─ longitude          (float)        - Geographic longitude     │
│                                                                 │
│ Temperature Information:                                        │
│ ├─ temperature        (float)        - Current temp (°C)        │
│ ├─ feels_like         (float)        - Perceived temp (°C)      │
│ ├─ temp_min           (float)        - Daily minimum (°C)       │
│ └─ temp_max           (float)        - Daily maximum (°C)       │
│                                                                 │
│ Atmospheric Data:                                               │
│ ├─ humidity           (int)          - Relative humidity (%)    │
│ ├─ pressure           (int)          - Atmospheric pressure     │
│ ├─ visibility         (float)        - Visibility (m)           │
│ └─ cloudiness         (int)          - Cloud coverage (%)       │
│                                                                 │
│ Wind Information:                                               │
│ ├─ wind_speed         (float)        - Wind speed (m/s)        │
│ ├─ wind_deg           (int)          - Wind direction (°)       │
│ ├─ wind_direction     (str)          - Cardinal direction       │
│ │                    (N/NE/E/SE/S/SW/W/NW)                    │
│ └─ wind_gust          (float)        - Gust speed (m/s)        │
│                                                                 │
│ Weather Condition:                                              │
│ ├─ main_condition     (str)          - Main weather (Clouds)    │
│ ├─ description        (str)          - Detailed description     │
│ ├─ icon               (str)          - Weather icon code        │
│ ├─ rain               (float)        - Rainfall (mm)            │
│ └─ snow               (float)        - Snowfall (mm)            │
│                                                                 │
│ Time Information:                                               │
│ ├─ sunrise            (str)          - Sunrise time             │
│ ├─ sunset             (str)          - Sunset time              │
│ ├─ timezone           (int)          - Timezone offset (hours)  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Characteristics:                                                │
│ - Created from OpenWeather API response                         │
│ - In-memory only (not persisted)                                │
│ - Immutable after creation                                      │
│ - Can be converted to Dict for JSON response                    │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                 FORECAST_DAY (In-Memory List)                   │
├─────────────────────────────────────────────────────────────────┤
│ date             (str)          - Date in YYYY-MM-DD format     │
│ day              (str)          - Day name (Monday, etc)        │
│ temperature      (float)        - Average temp (°C)             │
│ temp_max         (float)        - Maximum temp (°C)             │
│ temp_min         (float)        - Minimum temp (°C)             │
│ humidity         (int)          - Humidity (%)                  │
│ description      (str)          - Weather description           │
│ icon             (str)          - Weather icon code             │
│ wind_speed       (float)        - Wind speed (m/s)             │
│ rain_chance      (float)        - Precipitation probability (%) │
├─────────────────────────────────────────────────────────────────┤
│ Characteristics:                                                │
│ - List of 5 ForecastDay objects (5-day forecast)              │
│ - Created from OpenWeather forecast API response               │
│ - In-memory only (not persisted)                                │
│ - One object per forecast day                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Model Architecture
│     humidity    (int)   │
│     pressure    (int)   │
│     visibility  (float) │
│     wind_speed  (float) │
│     wind_deg    (int)   │
│     wind_gust   (float) │
│     cloudiness  (int)   │
│     condition   (str)   │
│     description (str)   │
│     icon        (str)   │
│     sunrise     (str)   │
│     sunset      (str)   │
│     rain        (float) │
│     snow        (float) │
│     timestamp   (date)  │
├─────────────────────────┤
│ Records weather search  │
└──────────────┬──────────┘
               │
               │ 1:Many
               │
┌──────────────▼──────────┐
│     FORECAST_DATA       │
├──────────────────────────┤
│ PK  forecast_id (str)   │
│ FK  search_id   (str)   │
│     date        (str)   │
│     day         (str)   │
│     temp_max    (float) │
│     temp_min    (float) │
│     temp        (float) │
│     humidity    (int)   │
│     description (str)   │
│     icon        (str)   │
│     wind_speed  (float) │
│     rain_chance (float) │
│     timestamp   (date)  │
├──────────────────────────┤
│ 5-day forecast records  │
└─────────────────────────┘


┌─────────────────────────┐
│    LOG_ENTRIES          │
├─────────────────────────┤
│ PK  log_id      (int)   │
│ FK  email       (str)   │
│     level       (str)   │
│     message     (str)   │
│     filename    (str)   │
│     lineno      (int)   │
│     timestamp   (date)  │
├─────────────────────────┤
│ Audit trail of events   │
└─────────────────────────┘
```

---

## Database Schema (Table Format)

### Table 1: USERS

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| email | VARCHAR(255) | PRIMARY KEY, UNIQUE, NOT NULL | User's email address |
| username | VARCHAR(100) | UNIQUE, NOT NULL | Display name |
| password | VARCHAR(255) | NOT NULL | Hashed password |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration date |

**Sample Data**:
```
┌──────────────────────────┬──────────┬──────────────────────┬─────────────────────┐
│ email                    │ username │ password             │ created_at          │
├──────────────────────────┼──────────┼──────────────────────┼─────────────────────┤
│ john@example.com         │ john_doe │ hashed_pwd_12345... │ 2025-12-10 10:30:00 │
│ jane@example.com         │ jane_dev │ hashed_pwd_67890... │ 2025-12-12 14:45:00 │
│ alice@example.com        │ alice123 │ hashed_pwd_abcde... │ 2025-12-14 09:15:00 │
└──────────────────────────┴──────────┴──────────────────────┴─────────────────────┘
```

**Indexes**:
- PRIMARY KEY (email)
- UNIQUE (username)
- INDEX (created_at)

---

### Table 2: SESSIONS

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| session_id | VARCHAR(255) | PRIMARY KEY | Unique session identifier |
| email | VARCHAR(255) | FOREIGN KEY (USERS) | User email |
| username | VARCHAR(100) | NOT NULL | Cached username |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Session start time |
| last_activity | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last action time |
| timeout | INT | DEFAULT 3600 | Timeout in seconds |
| ip_address | VARCHAR(45) | | IP address of client |
| user_agent | VARCHAR(500) | | Browser user agent |

**Sample Data**:
```
┌─────────────┬──────────────────┬──────────┬─────────────────────┬─────────────────────┬─────────┐
│ session_id  │ email            │ username │ created_at          │ last_activity       │ timeout │
├─────────────┼──────────────────┼──────────┼─────────────────────┼─────────────────────┼─────────┤
│ abc123def.. │ john@example.com │ john_doe │ 2025-12-14 10:00:00 │ 2025-12-14 10:45:30 │ 3600    │
│ xyz789ghi.. │ jane@example.com │ jane_dev │ 2025-12-14 11:30:00 │ 2025-12-14 11:55:00 │ 3600    │
└─────────────┴──────────────────┴──────────┴─────────────────────┴─────────────────────┴─────────┘
```

**Indexes**:
- PRIMARY KEY (session_id)
- FOREIGN KEY (email)
- INDEX (created_at)
- INDEX (last_activity)

---

### Table 3: WEATHER_DATA

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| search_id | VARCHAR(255) | PRIMARY KEY | Unique search identifier |
| email | VARCHAR(255) | FOREIGN KEY (USERS) | User who searched |
| city | VARCHAR(100) | NOT NULL | City name searched |
| country | VARCHAR(100) | NOT NULL | Country code |
| latitude | DECIMAL(10,6) | | City latitude |
| longitude | DECIMAL(10,6) | | City longitude |
| temperature | DECIMAL(5,2) | | Current temp (°C) |
| feels_like | DECIMAL(5,2) | | Feels like temp (°C) |
| temp_min | DECIMAL(5,2) | | Min temperature (°C) |
| temp_max | DECIMAL(5,2) | | Max temperature (°C) |
| humidity | INT | | Humidity (%) |
| pressure | INT | | Pressure (hPa) |
| visibility | DECIMAL(5,1) | | Visibility (km) |
| wind_speed | DECIMAL(5,2) | | Wind speed (m/s) |
| wind_deg | INT | | Wind direction (degrees) |
| wind_gust | DECIMAL(5,2) | | Wind gust (m/s) |
| cloudiness | INT | | Cloud coverage (%) |
| condition | VARCHAR(50) | | Weather condition |
| description | VARCHAR(255) | | Condition description |
| icon | VARCHAR(10) | | Weather icon code |
| sunrise | TIME | | Sunrise time |
| sunset | TIME | | Sunset time |
| rain | DECIMAL(5,2) | | Rain amount (mm) |
| snow | DECIMAL(5,2) | | Snow amount (mm) |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Search timestamp |

**Sample Data**:
```
┌──────────────┬──────────────────┬────────┬─────────┬───────────┬───────────┬─────────────┐
│ search_id    │ email            │ city   │ country │ latitude  │ longitude │ temperature │
├──────────────┼──────────────────┼────────┼─────────┼───────────┼───────────┼─────────────┤
│ search_001   │ john@example.com │ London │ GB      │ 51.5074   │ -0.1278   │ 12.5        │
│ search_002   │ jane@example.com │ Paris  │ FR      │ 48.8566   │ 2.3522    │ 10.2        │
│ search_003   │ john@example.com │ NewYork│ US      │ 40.7128   │ -74.0060  │ 8.5         │
└──────────────┴──────────────────┴────────┴─────────┴───────────┴───────────┴─────────────┘
```

**Indexes**:
- PRIMARY KEY (search_id)
- FOREIGN KEY (email)
- INDEX (city, timestamp)
- INDEX (created_at)

---

### Table 4: FORECAST_DATA

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| forecast_id | VARCHAR(255) | PRIMARY KEY | Unique forecast identifier |
| search_id | VARCHAR(255) | FOREIGN KEY (WEATHER_DATA) | Related weather search |
| date | DATE | NOT NULL | Forecast date |
| day | VARCHAR(20) | | Day of week |
| temp_max | DECIMAL(5,2) | | Max temperature (°C) |
| temp_min | DECIMAL(5,2) | | Min temperature (°C) |
| temp | DECIMAL(5,2) | | Average temperature (°C) |
| humidity | INT | | Humidity (%) |
| description | VARCHAR(255) | | Weather description |
| icon | VARCHAR(10) | | Weather icon code |
| wind_speed | DECIMAL(5,2) | | Wind speed (m/s) |
| rain_chance | DECIMAL(5,2) | | Probability of rain (%) |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record timestamp |

**Sample Data**:
```
┌──────────────┬──────────────┬────────────┬───────────┬──────────┬──────────┬──────────────┐
│ forecast_id  │ search_id    │ date       │ day       │ temp_max │ temp_min │ rain_chance  │
├──────────────┼──────────────┼────────────┼───────────┼──────────┼──────────┼──────────────┤
│ forecast_001 │ search_001   │ 2025-12-15 │ Monday    │ 16.5     │ 9.1      │ 20.0         │
│ forecast_002 │ search_001   │ 2025-12-16 │ Tuesday   │ 14.2     │ 7.8      │ 85.0         │
│ forecast_003 │ search_001   │ 2025-12-17 │ Wednesday │ 15.0     │ 8.5      │ 50.0         │
└──────────────┴──────────────┴────────────┴───────────┴──────────┴──────────┴──────────────┘
```

**Indexes**:
- PRIMARY KEY (forecast_id)
- FOREIGN KEY (search_id)
- INDEX (date)
- INDEX (timestamp)

---

### Table 5: LOG_ENTRIES

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| log_id | INT | PRIMARY KEY AUTO_INCREMENT | Log entry ID |
| email | VARCHAR(255) | FOREIGN KEY (USERS) | Associated user (nullable) |
| level | VARCHAR(20) | | Log level (DEBUG, INFO, etc.) |
| message | TEXT | NOT NULL | Log message |
| filename | VARCHAR(100) | | Source filename |
| lineno | INT | | Line number |
| exception | TEXT | | Exception details (nullable) |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Log timestamp |

**Sample Data**:
```
┌────────┬──────────────────┬─────────┬─────────────────────────┬──────────┬────────┐
│ log_id │ email            │ level   │ message                 │ filename │ lineno │
├────────┼──────────────────┼─────────┼─────────────────────────┼──────────┼────────┤
│ 1      │ john@example.com │ INFO    │ Successful login for... │ app.py   │ 150    │
│ 2      │ jane@example.com │ INFO    │ New user registered     │ app.py   │ 120    │
│ 3      │ NULL             │ ERROR   │ API request timeout     │ app.py   │ 245    │
│ 4      │ john@example.com │ DEBUG   │ Fetching weather for... │ app.py   │ 230    │
└────────┴──────────────────┴─────────┴─────────────────────────┴──────────┴────────┘
```

**Indexes**:
- PRIMARY KEY (log_id)
- FOREIGN KEY (email)
- INDEX (level, timestamp)
- INDEX (timestamp)

---

## Relationships

### One-to-Many Relationships

```
USERS (1) ────────→ (Many) SESSIONS
  ├─ One user can have multiple sessions
  └─ Foreign key: email

USERS (1) ────────→ (Many) WEATHER_DATA
  ├─ One user can search for weather multiple times
  └─ Foreign key: email

WEATHER_DATA (1) ──────→ (Many) FORECAST_DATA
  ├─ One weather search has 5 forecasts
  └─ Foreign key: search_id

USERS (1) ────────→ (Many) LOG_ENTRIES
  ├─ One user can have multiple log entries
  └─ Foreign key: email
```

---

## Normalization

### First Normal Form (1NF)
✅ All attributes are atomic (no multi-valued attributes)
✅ Each table has a primary key
✅ No repeating groups

### Second Normal Form (2NF)
✅ Meets 1NF
✅ All non-key attributes depend on the entire primary key

### Third Normal Form (3NF)
✅ Meets 2NF
✅ No transitive dependencies
✅ Non-key attributes depend only on the primary key

---

## Constraints

### Primary Keys
```sql
ALTER TABLE users ADD CONSTRAINT pk_users PRIMARY KEY (email);
ALTER TABLE sessions ADD CONSTRAINT pk_sessions PRIMARY KEY (session_id);
ALTER TABLE weather_data ADD CONSTRAINT pk_weather PRIMARY KEY (search_id);
ALTER TABLE forecast_data ADD CONSTRAINT pk_forecast PRIMARY KEY (forecast_id);
ALTER TABLE log_entries ADD CONSTRAINT pk_logs PRIMARY KEY (log_id);
```

### Foreign Keys
```sql
ALTER TABLE sessions 
ADD CONSTRAINT fk_sessions_users 
FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE;

ALTER TABLE weather_data 
ADD CONSTRAINT fk_weather_users 
FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE;

ALTER TABLE forecast_data 
ADD CONSTRAINT fk_forecast_weather 
FOREIGN KEY (search_id) REFERENCES weather_data(search_id) ON DELETE CASCADE;

ALTER TABLE log_entries 
ADD CONSTRAINT fk_logs_users 
FOREIGN KEY (email) REFERENCES users(email) ON DELETE SET NULL;
```

### Unique Constraints
```sql
ALTER TABLE users ADD CONSTRAINT uq_username UNIQUE (username);
ALTER TABLE users ADD CONSTRAINT uq_email UNIQUE (email);
```

### Check Constraints
```sql
ALTER TABLE weather_data ADD CONSTRAINT ck_humidity CHECK (humidity >= 0 AND humidity <= 100);
ALTER TABLE weather_data ADD CONSTRAINT ck_pressure CHECK (pressure > 0);
ALTER TABLE forecast_data ADD CONSTRAINT ck_rain CHECK (rain_chance >= 0 AND rain_chance <= 100);
```

---

## Data Types

| Field Type | Size | Range |
|---|---|---|
| VARCHAR(n) | n bytes | String up to n characters |
| INT | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| DECIMAL(p,s) | Variable | Precise decimal numbers |
| TIMESTAMP | 8 bytes | Date and time |
| DATE | 3 bytes | Date only |
| TIME | 3 bytes | Time only |
| TEXT | Variable | Large text (up to 65KB) |

---

## Query Examples

### Find User's Recent Searches
```sql
SELECT w.city, w.temperature, w.timestamp
FROM weather_data w
WHERE w.email = 'john@example.com'
ORDER BY w.timestamp DESC
LIMIT 10;
```

### Get Forecast for a Search
```sql
SELECT f.*
FROM forecast_data f
JOIN weather_data w ON f.search_id = w.search_id
WHERE w.search_id = 'search_001'
ORDER BY f.date ASC;
```

### Find Errors in Logs
```sql
SELECT *
FROM log_entries
WHERE level = 'ERROR'
ORDER BY timestamp DESC
LIMIT 20;
```

### User Activity Summary
```sql
SELECT 
  email,
  COUNT(DISTINCT search_id) as total_searches,
  MAX(timestamp) as last_search
FROM weather_data
GROUP BY email;
```

---

## Performance Optimization

### Indexes
```sql
-- Search optimization
CREATE INDEX idx_weather_city ON weather_data(city);
CREATE INDEX idx_weather_timestamp ON weather_data(timestamp);
CREATE INDEX idx_forecast_date ON forecast_data(date);

-- Join optimization
CREATE INDEX idx_sessions_email ON sessions(email);
CREATE INDEX idx_logs_email ON log_entries(email);

-- Query optimization
CREATE INDEX idx_logs_level_timestamp ON log_entries(level, timestamp);
```

### Partitioning Strategy
```sql
-- Partition by date for log entries (yearly)
PARTITION BY RANGE (YEAR(timestamp)) (
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

---

## Backup Strategy

### Daily Backups
```bash
mysqldump -u user -p weather_app > weather_app_$(date +%Y%m%d).sql
```

### Retention Policy
- Daily backups: 7 days
- Weekly backups: 4 weeks
- Monthly backups: 12 months

---

## Database Statistics

| Table | Est. Rows | Growth Rate | Size |
|-------|-----------|-------------|------|
| users | 100-1K | Slow | ~100 KB |
| sessions | 50-500 | Medium | ~50 KB |
| weather_data | 1K-10K | Medium | ~10 MB |
| forecast_data | 5K-50K | Medium | ~50 MB |
| log_entries | 10K-100K | Fast | ~100 MB |

---

## Migration Strategy

### Version Control
- Track schema changes in SQL migration files
- Use timestamps: `001_initial_schema.sql`, `002_add_columns.sql`
- Test migrations in development first

### Zero-Downtime Migrations
- Add new columns with DEFAULT values
- Migrate data gradually
- Remove old columns only after validation

---

## Summary

The database design is:
✅ **Normalized** (3NF)
✅ **Scalable** (indexed appropriately)
✅ **Maintainable** (clear relationships)
✅ **Secure** (constraints and validation)
✅ **Auditable** (log tracking)

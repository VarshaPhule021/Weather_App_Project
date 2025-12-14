# Weather App with Login System

## Features
- **User Authentication**: Sign up and login functionality
- **Weather Information**: Search for weather by city name
- **Session Management**: Users must login to access the weather feature
- **User Profile**: Display username in the app

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   - Edit `constant/header.py` and add your OpenWeather API key:
   ```python
   API_KEY = 'your_api_key_here'
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```
   The app will be available at `http://localhost:5000`

## User Flow

1. **Landing Page**: Users are redirected to `/login`
2. **Sign Up**: New users can create an account at `/signup`
3. **Login**: Users enter their email and password
4. **Dashboard**: After login, users access the weather search at `/weather`
5. **Logout**: Users can logout from the navigation bar

## Default Routes

- `/` - Redirects to login if not authenticated, otherwise to weather page
- `/login` - Login page
- `/signup` - Sign up page
- `/weather` - Weather search page (requires authentication)
- `/logout` - Logout route

## User Data Storage

Currently, user data is stored in `users.json` file. For production use, consider using a database like:
- SQLite
- PostgreSQL
- MongoDB

## Security Notes

⚠️ **Important**: The current implementation is for development only. For production:
1. Change the secret key in `app.py`
2. Hash passwords using libraries like `werkzeug.security` or `bcrypt`
3. Use HTTPS
4. Implement database instead of JSON files
5. Add CSRF protection

## Example Login Credentials (after signup)

After creating an account with:
- Email: user@example.com
- Password: password123

You can login with these credentials.

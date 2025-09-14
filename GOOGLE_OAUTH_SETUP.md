# Google OAuth Setup Guide

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API and Google OAuth2 API

## Step 2: Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in required information:
   - App name: "Smart Laundry"
   - User support email: your email
   - Developer contact: your email
4. Add scopes: `email`, `profile`
5. Add test users (for development)

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Add authorized redirect URIs:
   - `http://localhost:5000/api/auth/google/callback` (for development)
   - `https://yourdomain.com/api/auth/google/callback` (for production)
5. Copy the Client ID and Client Secret

## Step 4: Update Backend Configuration

Replace the placeholders in `laundry-backend/accounts/views.py`:

```python
GOOGLE_CLIENT_ID = "YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "YOUR_ACTUAL_CLIENT_SECRET"
```

## Step 5: Install Required Dependencies

Add to `laundry-backend/requirements.txt`:
```
requests>=2.25.1
```

Install:
```bash
pip install requests
```

## Step 6: Test the Integration

1. Start your backend server
2. Go to login page
3. Click "Continue with Google"
4. You should be redirected to Google's login page
5. After login, you'll be redirected back to your app

## Production Setup

For production, update:
1. Redirect URIs in Google Console
2. Client ID and Secret in backend
3. Frontend URL in callback redirect
4. Enable HTTPS for security

## Security Notes

- Never commit Client Secret to version control
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regularly rotate credentials







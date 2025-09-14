# Environment Variables Setup

## Required Environment Variables

Create a `.env` file in the `laundry-backend` directory with the following variables:

### Google OAuth Configuration
```bash
# Google OAuth Credentials (Get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-actual-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/api/auth/google/callback
```

### Django Settings
```bash
# Django Configuration
DEBUG=True
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
```bash
# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3
```

### Email Configuration
```bash
# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=admin@yourdomain.com
```

## How to Use

### 1. For Demo Mode (Current)
- Don't set any Google OAuth variables
- The system will automatically use demo mode
- Google login will create demo users

### 2. For Real Google OAuth
1. Get credentials from Google Cloud Console
2. Set the environment variables:
   ```bash
   GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-actual-client-secret
   ```
3. Restart the backend server
4. Google login will now use real Google accounts

## Environment Variable Priority

The system checks for environment variables in this order:
1. Environment variables from `.env` file
2. Default values (for demo mode)

## Security Notes

- Never commit `.env` file to version control
- Use strong, unique values for SECRET_KEY
- Keep Google credentials secure
- Use different credentials for development and production






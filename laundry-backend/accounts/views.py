from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


from django.core.mail import send_mail, BadHeaderError
import smtplib  # <- SMTPException ke liye
import random

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    if not email or not otp:
        return Response({"message": "email and otp required"}, status=status.HTTP_400_BAD_REQUEST)

    if not (isinstance(otp, str) and 4 <= len(otp) <= 6):
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    user, _created = User.objects.get_or_create(username=email, defaults={"email": email})

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    user_payload = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }
    return Response({"token": access_token, "user": user_payload})

# ================= UPDATED SEND OTP ===================
@api_view(["POST"])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get("email")
    if not email:
        return Response({"success": False, "message": "email required"}, status=400)

    # Generate random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    try:
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is {otp}",
            from_email="youremail@gmail.com",      # <-- apna Gmail yahan daal
            recipient_list=[email],
            fail_silently=False,
        )
        print(f"OTP sent to {email}: {otp}")  # Console me bhi dikhega
        return Response({"success": True, "otp": otp})  # Testing ke liye OTP response me bhi bhej sakte ho
    except BadHeaderError as e:
        print("EMAIL ERROR (BadHeader):", e)
        return Response({"success": False, "error": str(e)})
    except smtplib.SMTPException as e:  # <- Correct SMTPException
        print("EMAIL ERROR (SMTP):", e)
        return Response({"success": False, "error": str(e)})
    except Exception as e:
        print("EMAIL ERROR (Other):", e)
        return Response({"success": False, "error": str(e)})

@api_view(["GET"])
@permission_classes([AllowAny])
def google_oauth_start(request):
    # Google OAuth 2.0 implementation with environment variables
    from django.conf import settings
    import os
    
    # Get credentials from environment variables
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com')
    REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback')
    SCOPE = "email profile"
    
    # Check if we have real Google credentials
    if GOOGLE_CLIENT_ID == 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com':
        # Demo mode - create a simple demo flow
        import random
        import string
        demo_code = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        from django.http import HttpResponseRedirect
        callback_url = f"http://localhost:5000/api/auth/google/callback?code={demo_code}"
        return HttpResponseRedirect(callback_url)
    else:
        # Real Google OAuth flow
        google_oauth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={GOOGLE_CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"scope={SCOPE}&"
            f"response_type=code&"
            f"access_type=offline&"
            f"prompt=select_account"
        )
        
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(google_oauth_url)


@api_view(["GET"])
@permission_classes([AllowAny])
def google_oauth_callback(request):
    # Handle Google OAuth callback (both demo and real)
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        return Response({
            "success": False,
            "message": f"OAuth error: {error}"
        })
    
    if not code:
        return Response({
            "success": False,
            "message": "Authorization code not received"
        })
    
    try:
        import os
        from django.conf import settings
        
        # Get credentials from environment variables
        GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com')
        GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')
        REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback')
        
        print(f"Environment variables - CLIENT_ID: {GOOGLE_CLIENT_ID[:20]}..., SECRET: {GOOGLE_CLIENT_SECRET[:10]}..., REDIRECT: {REDIRECT_URI}")  # Debug logging
        
        # Check if we have real Google credentials
        if (GOOGLE_CLIENT_ID == 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com' or 
            GOOGLE_CLIENT_SECRET == 'YOUR_GOOGLE_CLIENT_SECRET'):
            # Demo mode - create a user with demo data
            import random
            import string
            
            # Generate demo user data with realistic names
            demo_names = [
                "Rajesh Kumar", "Priya Sharma", "Amit Singh", "Sneha Patel", 
                "Vikram Gupta", "Anita Reddy", "Suresh Kumar", "Kavita Joshi",
                "Ravi Verma", "Sunita Agarwal", "Manoj Tiwari", "Deepika Singh",
                "Arjun Mehta", "Pooja Shah", "Rohit Jain", "Neha Kapoor"
            ]
            demo_name = random.choice(demo_names)
            demo_email = f"{demo_name.lower().replace(' ', '.')}@gmail.com"
            
            # Create or get user
            user, _created = User.objects.get_or_create(
                username=demo_email,
                defaults={
                    "email": demo_email,
                    "first_name": demo_name.split()[0],
                    "last_name": demo_name.split()[-1] if len(demo_name.split()) > 1 else "",
                }
            )
            
            email = demo_email
            name = demo_name
            
        else:
            # Real Google OAuth flow
            import requests
            
            # Exchange authorization code for access token
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI,
            }
            
            print(f"Token exchange request: {token_data}")  # Debug logging
            
            token_response = requests.post(token_url, data=token_data)
            print(f"Token response status: {token_response.status_code}")  # Debug logging
            print(f"Token response content: {token_response.text}")  # Debug logging
            
            token_json = token_response.json()
            
            if 'access_token' not in token_json:
                return Response({
                    "success": False,
                    "message": f"Failed to get access token from Google. Error: {token_json.get('error', 'Unknown error')}. Description: {token_json.get('error_description', 'No description')}"
                })
            
            # Get user info from Google
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {'Authorization': f"Bearer {token_json['access_token']}"}
            user_response = requests.get(user_info_url, headers=headers)
            print(f"User info response status: {user_response.status_code}")  # Debug logging
            print(f"User info response content: {user_response.text}")  # Debug logging
            
            user_info = user_response.json()
            
            email = user_info.get('email')
            name = user_info.get('name', email)
            
            if not email:
                return Response({
                    "success": False,
                    "message": "Email not provided by Google"
                })
            
            # Create or get user
            user, _created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "first_name": user_info.get('given_name', ''),
                    "last_name": user_info.get('family_name', ''),
                }
            )
        
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        user_payload = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "name": name,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        
        # Redirect to frontend with token
        from django.http import HttpResponseRedirect
        frontend_url = f"http://localhost:3000/login?token={access_token}&email={email}&name={name}"
        return HttpResponseRedirect(frontend_url)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error processing login: {str(e)}"
        })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_users(request):
    """Get all users for admin dashboard"""
    if not request.user.is_staff:
        return Response({
            "success": False,
            "message": "Admin access required"
        }, status=403)
    
    try:
        users = User.objects.all().order_by('-date_joined')
        users_data = []
        
        for user in users:
            # Create full name from first_name and last_name
            full_name = f"{user.first_name} {user.last_name}".strip()
            if not full_name:
                full_name = user.email.split('@')[0]  # Fallback to email username
            
            users_data.append({
                "id": f"USR{user.id:03d}",
                "name": full_name,
                "email": user.email,
                "role": "Admin" if user.is_staff else "User",
                "date_joined": user.date_joined.strftime("%Y-%m-%d"),
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser
            })
        
        return Response({
            "success": True,
            "data": users_data
        })
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error fetching users: {str(e)}"
        }, status=500)

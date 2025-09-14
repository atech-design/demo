from django.urls import path
from .views import verify_otp, send_otp, google_oauth_start, google_oauth_callback, admin_users


urlpatterns = [
    path("send-otp", send_otp, name="send-otp"),
    path("verify-otp", verify_otp, name="verify-otp"),
    path("google", google_oauth_start, name="google-oauth-start"),
    path("google/callback", google_oauth_callback, name="google-oauth-callback"),
    path("admin/users", admin_users, name="admin-users"),
]



from django.urls import path
from otp_auth import views

urlpatterns = [
    path("request/", views.RequestOtp.as_view(), name='request-otp'),
    path("verify/", views.VerifyOtp.as_view(), name='verify-otp'),
]

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Future proofing the User Model."""
    pass


class PhoneUser(models.Model):
    """User class with mobile information."""
    user = models.OneToOneField(
        User, related_name="phone_user", on_delete=models.CASCADE)
    phone = models.CharField(max_length=32, unique=True, primary_key=True)


class UserProfile(models.Model):
    """Profile and other generic information of a user."""
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256,  null=True, blank=True)


class Otp(models.Model):
    """Class for Otp codes to be used for authentication."""
    otp_value = models.CharField(max_length=12, editable=False)
    generated_at = models.DateTimeField(auto_now_add=True, editable=False)
    phone = models.CharField(max_length=32, unique=True, primary_key=True)

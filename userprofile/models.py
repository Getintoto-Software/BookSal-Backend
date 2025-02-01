from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
import uuid


class UserProfile(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    # General User Information
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # use the email address to verify user. Only verified user can become futsal admin.
    email_address = models.EmailField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='images/profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    # User Contact Information
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    # Date Created and Updated
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # User Verification
    is_verified = models.BooleanField(default=False)
    is_futsal_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

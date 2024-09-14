from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']
    objects = UserManager()
    

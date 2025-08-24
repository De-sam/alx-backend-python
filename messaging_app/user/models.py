# user/models.py
from uuid import uuid4
from django.db import models
"""
This file contains the models for the user app
"""

class Role(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'

# Create your models here.
class User(models.Model):
    """
    This model is used to store the user details
    """
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=50, choices=Role.choices, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

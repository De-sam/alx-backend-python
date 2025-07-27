# uploads/models.py 
"""
This file contains the models for the uploads app
"""
from django.db import models
from chats.models import Chat
from user.models import User
# Create your models here.
class ReferenceType(models.TextChoices):
    CHAT = 'chat'
    USER = 'user'
    GROUP = 'group'

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/')
    #bind the reference_id to the model
    # reference_id = models.ForeignKey(User | Chat, on_delete=models.CASCADE, related_name='reference_id')
    reference_type = models.CharField(max_length=255, choices=ReferenceType.choices, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
# message/models.py
"""
This file contains the models for the message app
"""
from django.db import models
from user.models import User
from uuid import uuid4

class MessageType(models.TextChoices):
    TEXT = 'text'
    IMAGE = 'image'
    AUDIO = 'audio' 

class MessageStatus(models.TextChoices):
    PENDING = 'pending'
    SENT = 'sent'
    DELIVERED = 'delivered'
    READ = 'read'
    FAILED = 'failed'

# Create your models here.
class Message(models.Model):
    """
    This model is used to store the messages sent by the user to the user
    """
    message_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    message_body = models.CharField(max_length=255, null=False, blank=False)
    message_type = models.CharField(max_length=50, choices=MessageType.choices, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message_body

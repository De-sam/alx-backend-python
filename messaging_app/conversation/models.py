from django.db import models
from user.models import User
from uuid import uuid4
from chats.models import Chat

# Create your models here.
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    participants_id = models.ManyToManyField(User, related_name='participants')
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.conversation_id
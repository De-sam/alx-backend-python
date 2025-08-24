# chats/models.py
"""
This file contains the models for the chats app
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from message.models import Message
# from .models import Conversation
from django.conf import settings
# from uuid import uuid4

from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class MessageStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    DELIVERED = "delivered", "Delivered"
    READ = "read", "Read"

class Message(models.Model):
    """
    Represents a single message within a conversation.
    Updated to include a 'receiver' field for direct notifications.
    """
    
    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(
        settings.AUTH_CONVERSATION_MODEL, 
        on_delete=models.CASCADE, 
        related_name="messages",
        help_text="The conversation this message belongs to."
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="the user that sent this message"
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, #if user is deleted set to null
        related_name='received_messages',
        null=True,
        blank=True,
        help_text="The primary recipient of this message (optional, for direct notifications)."
    )
    message_body = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=MessageStatus.choices, default=MessageStatus.PENDING)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ["-sent_at"]
        constraints = [
            models.UniqueConstraint(fields=["message_id"], name="unique_message_id")
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.user if self.receiver else 'conversation'} in Conversation {self.conversation.id}"


class Notification(models.Model):
    """
    Represents a notification for a user, typically triggered by a new message.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="User who receives this notification"
        )
    message = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # delete notification if message is deleted
        help_text="the message that triggered this notification"
    )

    is_read = models.BooleanField(default=False, help_text="Indicates if the user have read the message")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="The timestamp when the notification was created")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notification for {self.user.username} about message {self.message.id} (Read: {self.is_read})"

    
class Conversation(models.Model):
    """
    This model is used to store the conversation details
    """

    conversation_id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations",
        help_text=_("Users participating in this conversation"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractBaseUser, PermissionsMixin):
    """
    This model is used to store the user details
    """

    # this fields are inherited from the AbstractUser class
    user_id = models.AutoField(primary_key=True)
    
    # this field is inherited from the AbstractUser class
    first_name = models.CharField(
        _("first name"),
        max_length=255,
        null=False,
        blank=False,
        help_text=_("User's first name"),
    )

    last_name = models.CharField(
        _("last name"),
        max_length=255,
        null=False,
        blank=False,
        help_text=_("User's last name"),
    )
    # this field is inherited from the AbstractUser class
    email = models.EmailField(
        _("email address"),
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        help_text=_("User's email address"),
    )
    # this field is not inherited from the AbstractUser class
    phone_number = models.CharField(
        _("phone number"),
        max_length=15,
        null=False,
        blank=False,
        unique=True,
        help_text=_("User's phone number, e.g., +12125551212"),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email")
        ]

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.pk}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


# Create your models here.
class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="chats"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.message)

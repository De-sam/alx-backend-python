# chats/models.py
"""
This file contains the models for the chats app
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from message.models import Message
from django.conf import settings
# from uuid import uuid4

# from chats.models import User # WATCHOUT: user defined in settings.py as Auth_User_Model might handle this differently
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
    This model stores the details of messages sent between users.

    Fields:
        message_id (int): Primary key for each message.
        sender (User): The user who sends the message.
        receiver (User): The user who receives the message.
        content (str): The body of the message.
        status (str): Delivery status (Pending, Sent, etc.).
        timestamp (datetime): When the message was sent.
        edited (bool): Whether the message has been edited.
        edited_by (User): The user who edited the message.
        parent_message (Message): The message this one is replying to.
    """

    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    status = models.CharField(max_length=20, choices=MessageStatus.choices, default=MessageStatus.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="edited_messages")

    # 👇 New field for threaded replies
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        help_text=_("The parent message this is replying to")
    )

    class Meta:
        ordering = ["-timestamp"]


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


class Notification(models.Model):
    """
    This model is used to store user notifications for new messages.
    A notification is created whenever a new Message instance is saved.
    """

    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text=_("The user who will receive the notification"),
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text=_("The message that triggered the notification"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date and time when the notification was created"),
    )
    read = models.BooleanField(
        default=False,
        help_text=_("Indicates whether the notification has been read by the user"),
    )

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user} on message {self.message_id}"


class MessageHistory(models.Model):
    """
    This model stores the previous versions of edited messages.
    
    Fields:
        history_id (int): Primary key for the history record.
        message (Message): The message that was edited.
        old_content (str): The content before the edit.
        edited_at (datetime): Timestamp of the edit.
    """
    history_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history',
        help_text=_("The message that was edited"),
    )
    old_content = models.TextField(help_text=_("The content before the edit"))
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message {self.message_id} at {self.edited_at}"

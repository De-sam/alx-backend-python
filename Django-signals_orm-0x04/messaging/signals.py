"""
This file defines signal handlers for the chats app.

Signal:
    post_save (Message) – Triggers when a new message is created and sends a notification to the receiver.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from chats.models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def notify_receiver_on_new_message(sender, instance: Message, created: bool, **kwargs):
    """
    Creates a Notification for the receiver when a new Message is sent.

    Args:
        sender (Model class): The model class that sent the signal.
        instance (Message): The actual instance being saved.
        created (bool): A boolean indicating if the instance was created.
        **kwargs: Additional keyword arguments.

    Behavior:
        - If a new Message is created, a corresponding Notification is created
          for the `receiver` of the message.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )



@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance: Message, **kwargs):
    """
    Logs the previous version of a message before it is updated.

    Args:
        sender (Model class): The model class sending the signal.
        instance (Message): The message instance being saved.
        **kwargs: Additional keyword arguments.

    Behavior:
        - If the message already exists (i.e., being updated),
          and content has changed, save the old version in MessageHistory.
    """
    if not instance.pk:
        return  # Skip new message creation

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        # Log old content
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance: User, **kwargs):
    """
    Deletes all messages, notifications, and message histories
    related to a user when their account is deleted.

    Args:
        sender (Model class): The model class that sent the signal.
        instance (User): The user instance being deleted.
        **kwargs: Additional keyword arguments.
    """

    # Delete sent and received messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications
    Notification.objects.filter(user=instance).delete()

    # Delete message history for messages the user sent
    MessageHistory.objects.filter(message__sender=instance).delete()

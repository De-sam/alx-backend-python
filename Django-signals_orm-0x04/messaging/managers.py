# messaging/managers.py

from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to retrieve unread messages for a specific user.
    """

    def unread_for_user(self, user):
        return self.get_queryset().filter(
            receiver=user, read=False
        ).only("message_id", "sender", "receiver", "content", "timestamp")

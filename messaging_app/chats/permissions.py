# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If object is a Message, check if user is part of the related conversation
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        # If object is a Conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        return False

    def has_permission(self, request, view):
        # Global check to ensure the user is authenticated
        return request.user and request.user.is_authenticated

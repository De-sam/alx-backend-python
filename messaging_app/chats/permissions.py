# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only conversation participants to access/modify.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Message or Conversation object
        conversation = getattr(obj, 'conversation', obj)  # If obj is Message, use .conversation

        # Read-only methods: GET, HEAD, OPTIONS are always allowed for participants
        if request.method in permissions.SAFE_METHODS:
            return user in conversation.participants.all()

        # Write methods: POST, PUT, PATCH, DELETE
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return user in conversation.participants.all()

        return False

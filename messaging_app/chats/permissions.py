from rest_framework import permissions
from oauth2_provider.contrib.rest_framework import TokenHasScope as BaseTokenHasScope
from django.core.exceptions import ImproperlyConfigured

class TokenHasScope(BaseTokenHasScope):
    """
    Custom TokenHasScope that properly handles HTTP method-specific scopes
    """
    def get_scopes(self, request, view):
        try:
            required_scopes = getattr(view, "required_scopes")
            # Get scopes for the current HTTP method
            current_method_scopes = required_scopes.get(request.method, [])
            return current_method_scopes
        except AttributeError:
            raise ImproperlyConfigured(
                "TokenHasScope requires the view to define the required_scopes attribute"
            )


class isParticipantOfConversation(permissions.BasePermission):
    """
    custom permission to allow only participants of a conversation
    to update, delete, add reaction within a conversation
    """

    def has_permission(self, request, view):
        """
        Global permission to protect list view routes e.g GET /messages
        verify user is authenicated, first layer auth
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        read message object, ensure the message is read by its perticipant
        """

        if not (request.user and request.user.is_authenticated):
            return False
        
        #determine object type
        conversation = None
        if hasattr(obj, 'conversation'): #check if object is a message obj
            conversation = obj.conversation
        if hasattr(obj, 'participants'): #check if object is a conversation object
            conversation = obj
        if not conversation:
            return False
        
        #validate request user is a participant of conversation
        is_participant = request.user in conversation.participants.all()

        if request.method in permissions.SAFE_METHODS: #check request method and grant participants access
            return is_participant 
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant
        elif request.method == 'POST':
            return is_participant
        
        return False




    
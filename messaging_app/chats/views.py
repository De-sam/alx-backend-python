# chats/views.py
"""
This file contains the views for the chats app
"""

from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message, Chat
from .permissions import TokenHasScope
from rest_framework.response import Response
# filters for the models
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from pprint import pprint
import logging

# Set up logger for token scope debugging
logger = logging.getLogger(__name__)

# serializers for the models
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer,
    ChatSerializer,
)

# import permissions
from .permissions import isParticipantOfConversation


def log_token_scopes(request, view_name, view_class=None):
    """
    Log the token scopes for debugging purposes
    """
    logger.info(f"[{view_name}] HTTP Method: {request.method}")
    
    # Also print to console for immediate visibility during development
    print(f"\n=== TOKEN SCOPE DEBUG [{view_name}] ===")
    print(f"HTTP Method: {request.method}")
    print(f"Request URL: {request.path}")
    
    if hasattr(request, 'auth') and request.auth:
        token = request.auth
        if hasattr(token, 'scope'):
            print(f"Token scopes: {token.scope}")
            print(f"Token is valid: {token.is_valid()}")
            print(f"Token is expired: {token.is_expired()}")
            
            logger.info(f"[{view_name}] Token: {token}")
            
            logger.info(f"[{view_name}] Token scopes: {token.scope}")
            logger.info(f"[{view_name}] Token is valid: {token.is_valid()}")
            logger.info(f"[{view_name}] Token is expired: {token.is_expired()}")
            
            # Get required scopes from the view class if provided
            if view_class and hasattr(view_class, 'required_scopes'):
                required_scopes = getattr(view_class, 'required_scopes', {})
                current_method_scopes = required_scopes.get(request.method, [])
                print(f"Required scopes for {request.method}: {current_method_scopes}")
                print(f"All required scopes: {required_scopes}")
                logger.info(f"[{view_name}] Required scopes for {request.method}: {current_method_scopes}")
                logger.info(f"[{view_name}] All required scopes: {required_scopes}")
                
                # Test the actual token.is_valid() call that TokenHasScope uses
                print(f"Testing token.is_valid({current_method_scopes}): {token.is_valid(current_method_scopes)}")
                logger.info(f"[{view_name}] token.is_valid({current_method_scopes}): {token.is_valid(current_method_scopes)}")
                
                # Show what TokenHasScope actually receives
                print(f"TokenHasScope receives: required_scopes = {required_scopes}")
                logger.info(f"[{view_name}] TokenHasScope receives: required_scopes = {required_scopes}")
            else:
                print(f"No required_scopes found for {view_name}")
                logger.info(f"[{view_name}] No required_scopes found")
        else:
            print("Token has no scope attribute")
            logger.warning(f"[{view_name}] Token has no scope attribute")
    else:
        print("No token found in request")
        logger.warning(f"[{view_name}] No token found in request")
    
    print("=== END TOKEN SCOPE DEBUG ===\n")


def test_logging(request):
    """
    Simple test endpoint to verify logging is working
    """
    log_token_scopes(request, "TestEndpoint")
    return HttpResponse("Logging test completed - check console and debug.log")


def filter_by_user(queryset, user_id):
    """
    Filter the queryset by the user id
    """
    return queryset.filter(user_id=user_id)


def filter_by_conversation(queryset, conversation_id):
    """
    Filter the queryset by the conversation id
    """
    return queryset.filter(conversation=conversation_id)


def filter_by_message(queryset, message_id):
    """
    Filter the queryset by the message id
    """
    return queryset.filter(message=message_id)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
        ]
    
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user_id"]

    def get_queryset(self):
        """
        Filter the queryset by the user id
        """
        print(self.request.user)
        # Convert data to a readable string
        return filter_by_user(self.queryset, self.request.user.user_id)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasScope,
        isParticipantOfConversation,
    ]

    required_scopes = {
        "GET": ["read:messages"],
        "POST": ["manage:conversations"],
        "PUT": ["manage:conversations"],
        # "PATCH": ["manage:conversations"],
        # "DELETE": ["manage:conversations"],
    }

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation_id"]

    def get_queryset(self):
        """
        Filter the queryset by the user's conversations
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(participants=user).distinct()
        return Conversation.objects.none()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasScope,
        isParticipantOfConversation,
    ]

    required_scopes = {
        'GET': ['read:messages'],
        'POST': ['send:messages'],
        'PUT': ['send:messages', 'manage:conversations'],
        'PATCH': ['send:messages', 'manage:conversations'],
        'DELETE': ['manage:conversations']
    }

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation", "status"]

    def perform_create(self, serializer):
        """
        use Current  User as message sender
        add as participant
        """

        conversation = serializer.validated_data.get('conversation')

        # check user is authenticated, general authentication
        if not self.request.user.is_authenticated:
            return Response({'detail': "Action not authorised, login and try again"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        # check request user is a participant of conversation
        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            return Response({'detail': 'You are not a participant of this conversation'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        logger.info(f"[{self.request.user.user_id}] Sending message to conversation: {conversation.conversation_id}")
        
        serializer.save(status="sent")

    def perform_update(self, serializer):
        """
        update conversation, conversation can only be updated by a perticipant
        """

        #retrieve message object
        message_obj = self.get_object() 

        #manually check participants
        if not Message.objects.filter(message_id=message_obj.message_id, conversation__participants=self.request.user).exists():
            return Response({"detail": "Action denied due to you are not a participant of this conversation"}, 
                            status=status.HTTP_403_FORBIDDEN)        
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handle delete conversation, verify request user is authorised 
        """
        if not Message.objects.filter(message_id=instance.message_id, conversation__participants=self.request.user).exists():
            return Response({'detail', "Action is Unauthorised"}, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()

    def get_queryset(self):
        """
        Filter the queryset by the user's conversations
        """
        user = self.request.user
        if  user.is_authenticated:
            user_conversation = Conversation.objects.filter(participants=user)
            return Message.objects.filter(conversation__in=user_conversation)
        return Message.objects.none()

class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint to returns chat history.
    """

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["message"]

    def get_queryset(self):
        """
        Filter the queryset by the user's messages
        """
        return self.queryset.filter(
            message__conversation__participants=self.request.user
        )

#!/usr/bin/env python3
"""Viewsets for messaging app"""

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message
from chats.serializers import ConversationSerializer, MessageSerializer
from chats.permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations"""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Only return conversations the user participates in"""
        return self.request.user.conversations.all()

    def perform_create(self, serializer):
        """When a conversation is created, add the requesting user as a participant"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to the conversation"""
        conversation = self.get_object()
        user = request.user
        conversation.participants.add(user)
        conversation.save()
        return Response({'status': 'participant added'})


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Only return messages from conversations the user participates in"""
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """Only allow users to send messages in conversations they are part of"""
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)

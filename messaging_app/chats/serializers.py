#!/usr/bin/env python3
"""Serializers for messaging app"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serialize user info (excluding password_hash by default)"""

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    """Serialize messages"""

    sender = UserSerializer(read_only=True)  # show nested sender info

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serialize conversations with nested participants and messages"""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

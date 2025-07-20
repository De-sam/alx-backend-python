#!/usr/bin/env python3
"""Serializers for messaging app"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with password handling and role validation"""

    password = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'role', 'password', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_role(self, value):
        if value not in ['guest', 'host', 'admin']:
            raise serializers.ValidationError("Role must be guest, host, or admin.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.password_hash = user.password
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""

    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'conversation']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages"""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

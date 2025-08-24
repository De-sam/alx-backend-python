# chats/serializers.py
"""
This file contains the serializers for the chats app
"""

from rest_framework import serializers
from .models import User, Conversation, Message, Chat


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["user_id"]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation objects.
    Handles nested messages and custom fields.
    """
    # this field is not inherited from the AbstractConversation class
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        many=True,
        help_text=("IDs of users participating in this conversation")
        )
    # this field is not inherited from the AbstractConversation class
    participants_count = serializers.SerializerMethodField()
    # this field is not inherited from the AbstractConversation class
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "participants_count", "last_message_preview", "created_at", "updated_at"]
        read_only_fields = ["conversation_id"]

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_last_message_preview(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return last_message.message_body[:50] + "..." if len(last_message.message_body) > 50 else last_message.message_body
        return "No messages yet"

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model
    """
    # this field is not inherited from the AbstractMessage class
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        help_text=("The conversation this message belongs to")
    )
    # this field is not inherited from the AbstractMessage class
    message_body = serializers.CharField(
        max_length=1000,
        min_length=1,
        help_text=("The content of the message")
    )

    # this field is not inherited from the AbstractMessage class
    def validate_message_body(self, value):
        """
        Validate the content of the message
        """
        if not value.strip():
            raise serializers.ValidationError("Message content is required")
        if len(value) > 1000:
            raise serializers.ValidationError("Message content is too long")
        return value
    
    # this field is not inherited from the AbstractMessage class
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["message_id"]

class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chat model
    """

    class Meta:
        model = Chat
        fields = "__all__"

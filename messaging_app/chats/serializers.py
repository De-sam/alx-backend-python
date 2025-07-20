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
        """Compute full name"""
        return f"{obj.first_name} {obj.last_name}"

    def validate_role(self, value):
        """Ensure role is valid"""
        if value not in ['guest', 'host', 'admin']:
            raise serializers.ValidationError("Role must be guest, host, or admin.")
        return value

    def create(self, validated_data):
        """Override to handle password properly"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.password_hash = user.password  # Store the hashed password
        user.save()
        return user

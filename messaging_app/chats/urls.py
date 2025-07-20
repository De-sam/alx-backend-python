#!/usr/bin/env python3
"""Routing for chats app with nested router"""

from django.urls import path, include
from rest_framework_nested import routers 
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

convo_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
]

#!/usr/bin/env python3
"""Project-level URLs"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # ✅ Mount all API endpoints under /api/
]

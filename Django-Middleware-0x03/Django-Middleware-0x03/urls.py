# NOTE: this File is for Savanna Tests not in used by the application due to the name combination

"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # OAuth2 provider URLs
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # api
    path('api/', include('chats.urls')),

    # Include chats app URLs
    # path('api/', include('chats.urls')),
    # path('api/auth/', auth_views.obtain_auth_token),
]

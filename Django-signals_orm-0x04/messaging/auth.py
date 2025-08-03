"""
This file contains the authentication classes for the chats app
"""

from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    """
    This class is used to authenticate the user using the token
    """
    keyword = 'Bearer'
    
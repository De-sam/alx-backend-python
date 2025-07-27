# chats/filters.py

import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_at__gte = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at__lte = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sent_at__gte', 'sent_at__lte']

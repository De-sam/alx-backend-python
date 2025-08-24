import django_filters
from .models import Conversation, Message
from django.conf import settings

class MessageFilter(django_filters.FilterSet):
    """
    Filter class for Message model
    allows filtering by perticipants_id and date range
    """

    perticipants_ids =django_filters.CharFilter(
        method='filter_by_perticipants',
        help_text='provide a list of comma separated participants uuids to filter message'
    )

    start_date = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte', #less than or equal to
        help_text='Select date to filter conversation by date'
    )

    end_date = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte', # less than or equal to
        help_text='select end date (ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ).)'
    )

    class Meta:
        model = Message
        # define filterable fields
        fields = ['participants_ids', 'start_date', 'end_date']

    def filter_by_participants(self, queryset, name, value):
        """
        handle Conversation filter by participants
        """

        participant_ids = [ids.strip() for ids in value.split(',') if ids.strip()] 

        if not participant_ids:
            return queryset #return unfiltered conversation response if no ids is given
        
        filter_conversation = Conversation.objects.filter(
            participant__ids__in=participant_ids
            ).distinct()
        
        # filtered conversation list from applied participants Ids
        return filter_conversation
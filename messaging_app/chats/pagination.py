from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class to set a default page size for messages,
    inheriting from BasePagination and explicitly setting the count.
    """
    
    page_size = 20
    # page_size_query_param='page_size'
    # max_page_size=100
    
    def get_paginated_response(self, data):
        """
        wrap response with a paginated response
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data 
        })
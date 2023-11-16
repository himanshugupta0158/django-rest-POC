import string
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from rest_framework import viewsets, views
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.filters import BaseFilterBackend, SearchFilter, OrderingFilter
from .serializers import UserSerializer, GroupSerializer, RandomUserSerializer, SearchSerializer
import random
# 3rd party
from faker import Faker
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import F, Q, Value, OuterRef, Subquery

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class Generate_Random_Users(views.APIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = RandomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        fake = Faker()
        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = first_name+" "+last_name
            email = first_name+last_name+str(random.randint(1,9999))+"@gmail.com"
            is_active = random.choice([True, False])

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=is_active,
            )

            password = User.objects.make_random_password()
            print(password)
            user.set_password(password)
            user.save(update_fields=['password'])
            
        return Response({"Message" : "100 Users Created Successfully."})
    
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class SearchUser(views.APIView):
    queryset = User.objects.all().order_by('-date_joined')
    # serializer_class = SearchSerializer
    serializer_class = RandomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    # filter_class = filter_custom_class
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    
    def get(self, request, key):

        # Filter users based on the search key
        data = User.objects.filter(Q(username__contains=key))
        
        # Paginate the data
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, request)

        # Serialize the paginated data
        serializer = RandomUserSerializer(page, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)






import string
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from rest_framework import viewsets, views
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import mixins

from .paginations import StandardResultsSetPagination

from .filters import UserFilter
from .serializers import (
    UserSerializer,
    GroupSerializer,
    RandomUserSerializer,
    StudentSerializer,
)
import random

# 3rd party
from faker import Faker
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet

# in-build django rest filter
from rest_framework.filters import BaseFilterBackend, SearchFilter, OrderingFilter


from django.db.models import F, Q, Value, OuterRef, Subquery
from .models import Student


class StudentList(ListAPIView,CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "roll", "city"]
    # filter_backends = (
    # DjangoFilterBackend,
    # SearchFilter,
    # OrderingFilter,
    # )

    # def get_queryset(self):
    ## for allowing only logged in user related student data to be shown up.
    #     user = User.objects.get(username=self.request.user)
    #     print(f"User : {user}")
    #     return Student.objects.filter(passby=user.id)

    def get(self, request,pk=None, *args, **kwargs):
        if not pk :
            return self.list(request, *args, **kwargs)
        else:
            return self.retrieve(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Creating Student CRUD API using mixins and Generic API Views
class StudentView(
    GenericAPIView,
    mixins.ListModelMixin
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = StandardResultsSetPagination
    filterset_class = UserFilter
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    # search_fields = ['username', 'email'] # not working properly


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class Generate_Random_Users(views.APIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = RandomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        fake = Faker()
        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = first_name + " " + last_name
            email = first_name + last_name + str(random.randint(1, 9999)) + "@gmail.com"
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
            user.save(update_fields=["password"])

        return Response({"Message": "100 Users Created Successfully."})


class SearchUser(views.APIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = RandomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    # filter_backends = [DjangoFilterBackend]  # not working

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilter
    # search_fields = ['username', 'email']

    def get_queryset(self, queryset=None):
        # Apply filters to the queryset based on the request
        if queryset is None:
            queryset = User.objects.all().order_by("-date_joined")
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset

    def get(self, request, key):
        # ---------------------------------
        #  ----- Putting random data of student -----
        # fake = Faker()
        # for _ in range(50):
        #     Student.objects.create(
        #         name = fake.name(),
        #         roll = random.randint(10000,99999),
        #         city = fake.city(),
        #         passby = random.randint(502,701)
        #     )
        # ---------------------------------

        # Filter users based on the search key
        data = User.objects.filter(Q(username__contains=key))

        queryset = self.get_queryset(data)

        # Paginate the filtered data
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        # Serialize the paginated data
        serializer = RandomUserSerializer(page, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)

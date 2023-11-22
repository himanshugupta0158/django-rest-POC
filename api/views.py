import string
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from rest_framework import viewsets, views
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action

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


from django.db.models import F, Q, Value, OuterRef, Subquery, Avg, Count
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
    #     return Student.objects.filter(passed_by=user.id)

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
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # pagination_class = StandardResultsSetPagination # pagination
    # Adding filters and  All Filters are working
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    
    # Filter by name, roll and city 
    filterset_fields = ["name", "roll", "city"] # add which filter field to be added

    # Search Filter requirements
    search_fields = ["name", "roll"]


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class StudentDetailView(
    GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def search_by_name(self, request, name):
        students = Student.objects.filter(name__icontains=name)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    def filter_by_passby(self, request, passby):
        students = Student.objects.filter(passed_by=passby)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    def sort_students(self, request, field):
        students = Student.objects.order_by(field)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    def group_students(self, request, field):
        grouped_students = Student.objects.values(field).annotate(count=Count(field))
        return Response(grouped_students)

    @action(detail=False, methods=["get"])
    def total_students_count(self, request):
        total_count = Student.objects.count()
        return Response({'total_students': total_count})

    
    def distinct_values(self, request, field):
        distinct_values = Student.objects.values(field).distinct()
        return Response(distinct_values)

    @action(detail=False, methods=["get"])
    def random_student(self, request):
        random_student = random.choice(Student.objects.all())
        serializer = self.get_serializer(random_student)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def student_statistics(self, request):
        statistics = Student.objects.aggregate(average_marks=Avg('roll'), total_students=Count('id')) # F is used
        statistics["total_passed"] = Student.objects.filter(marks__gte=0.33*1600).count()
        return Response(statistics)

    def recent_students(self, request, count):
        recent_students = Student.objects.order_by('-id')[:count]
        serializer = self.get_serializer(recent_students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def pass_percentage(self, request):
        total_students = Student.objects.count()
        passed_students = Student.objects.filter(marks__gte=0.33 * 1600).count()
        passed_with_Agrade = Student.objects.filter(marks__gte=0.80 * 1600).count()
        passed_with_Bgrade = Student.objects.filter(marks__gte=0.70 * 1600).count()
        passed_with_Cgrade = Student.objects.filter(marks__gte=0.60 * 1600).count()
        passed_with_Dgrade = Student.objects.filter(marks__gte=0.45 * 1600).count()
        passed_with_Egrade = Student.objects.filter(marks__gte=0.33 * 1600).count()
        passed_with_Fgrade = Student.objects.filter(marks__lt=0.33 * 1600).count()
        print(f"Total Passed Students : {passed_students}")
        pass_percentage = (passed_students / total_students) * 100 if total_students > 0 else 0
        return Response({
            "Total Students" : total_students,
            'Total pass_percentage': pass_percentage,
            'Total A Grade' : passed_with_Agrade,
            'Total B Grade' : passed_with_Bgrade,
            'Total C Grade' : passed_with_Cgrade,
            'Total D Grade' : passed_with_Dgrade,
            'Total E Grade' : passed_with_Egrade,
            'Total F Grade' : passed_with_Fgrade,
            })

    # Override the default 'list' method for custom operations
    def list(self, request, *args, **kwargs):

        # for std in self.queryset:
        #     # std.passed_by = random.choice(User.objects.all())
        #     std.marks = random.choice([i for i in range(250, 1600)])
        #     std.save()

        return super().list(request, *args, **kwargs)


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
    queryset = User.objects.all().order_by("username")
    serializer_class = RandomUserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserFilter


    def get_queryset(self, queryset=None):
        # Apply filters to the queryset based on the request
        if queryset is None:
            queryset = User.objects.all().order_by("-date_joined")
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset


    def get(self, request, key):

        # Filter users based on the search key
        data = User.objects.filter(Q(username__contains=key))

        # Filter apply 
        data = self.get_queryset(data)

        # Serialize data
        serializer = RandomUserSerializer(data, many=True)

        # Return the paginated response
        return Response(serializer.data)


class SearchUserWithPaginationAndFilters(views.APIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = RandomUserSerializer
    # permission_classes = [permissions.IsAuthenticated]
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
        #         marks = random.choice([i for i in range(250, 1600)]),
        #         passed_by = random.choice(User.objects.all())
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
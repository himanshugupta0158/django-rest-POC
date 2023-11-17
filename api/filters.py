from django_filters.filters import CharFilter, BooleanFilter
from django.contrib.auth.models import User
from django_filters import FilterSet

class UserFilter(FilterSet):
    username = CharFilter(lookup_expr='contains', field_name='username')
    email = CharFilter(lookup_expr='contains', field_name='email')
    # is_active = BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ['username', 'email']



# class StudentFilter(FilterSet):
#     class Meta:
#         model = Student
#         fields = ['name', 'roll', 'city']
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Student

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RandomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    search = serializers.CharField()

    class Meta:
        fields = ['search']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'city', 'passby']
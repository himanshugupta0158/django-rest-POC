from django.db import models
import random
from django.contrib.auth.models import User



class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.IntegerField()
    city = models.CharField(max_length=50)
    marks = models.IntegerField(null=True, blank=True)
    passed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # def search_by_name(self, name):
    #     return Student.objects.filter(models.Q(name__contains=name))
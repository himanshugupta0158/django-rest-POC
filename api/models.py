from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.IntegerField()
    city = models.CharField(max_length=50)
    passby = models.CharField(max_length=50)

    def search_by_name(self, name):
        return Student.objects.filter(models.Q(name__contains=name))
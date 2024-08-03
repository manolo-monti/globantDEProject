from django.db import models

# Create your models here.
class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=250)

class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    job = models.CharField(max_length=250)

class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
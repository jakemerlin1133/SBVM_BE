from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    password= models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bottle_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class StudentToken(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.student.student_id} - Token"

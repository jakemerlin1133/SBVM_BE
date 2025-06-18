# users/serializers.py

from rest_framework import serializers
from .models import Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

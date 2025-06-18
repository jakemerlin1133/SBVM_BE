from rest_framework import serializers
from .models import Student

# For login only: accepts student_id and password
class LoginSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    password = serializers.CharField()

# For the ViewSet (admin/API browsing)
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

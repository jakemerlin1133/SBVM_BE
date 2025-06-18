from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from .models import Student
from .serializers import LoginSerializer, StudentSerializer


# --- GET ALL Students View ---
@api_view(['GET'])
def get_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


# --- ADD Student ---
@api_view(['POST'])
def add_student(request):
    data = request.data
    if 'password' in data:
        data['password'] = make_password(data['password'])

    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- GET / UPDATE / DELETE Student by ID ---
@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = StudentSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response({'message': 'Student deleted successfully'})
    

# --- LOGIN ---
@api_view(['POST'])
def student_login(request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    student_id = serializer.validated_data['student_id']
    password = serializer.validated_data['password']

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    if not check_password(password, student.password):
        return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'message': 'Login successful',
        'student_id': student.student_id
    })
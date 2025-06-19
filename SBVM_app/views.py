from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from .models import Student
from .serializers import LoginSerializer, StudentSerializer
from rest_framework.authtoken.models import Token

import secrets
from .models import StudentToken


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
        return Response({
            'message': 'Invalid input',
            'errors': serializer.errors,
            'status_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)

    student_id = serializer.validated_data['student_id']
    password = serializer.validated_data['password']

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response({
            'message': 'Student not found',
            'status_code': 404
        }, status=status.HTTP_404_NOT_FOUND)

    if not check_password(password, student.password):
        return Response({
            'message': 'Invalid password',
            'status_code': 401
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Set is_active to True
    student.is_active = True
    student.save()

    # Generate or retrieve token manually
    token_obj, created = StudentToken.objects.get_or_create(student=student)

    if not created:
        token = token_obj.token
    else:
        token = secrets.token_hex(16)
        token_obj.token = token
        token_obj.save()

    return Response({
        'message': 'Login successful',
        'student_id': student.student_id,
        'token': token,
        'status_code': 200
    }, status=status.HTTP_200_OK)



# --- LOGOUT ---
@api_view(['POST'])
def student_logout(request):
    student_id = request.data.get('student_id')

    if not student_id:
        return Response({
            'message': 'Student ID is required',
            'status_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response({
            'message': 'Student not found',
            'status_code': 404
        }, status=status.HTTP_404_NOT_FOUND)

    # Set student as inactive
    student.is_active = False
    student.save()

    # Remove token if it exists
    try:
        token = StudentToken.objects.get(student=student)
        token.delete()
        token_deleted = True
    except StudentToken.DoesNotExist:
        token_deleted = False

    return Response({
        'message': 'Logout successful',
        'student_id': student.student_id,
        'token_deleted': token_deleted,
        'status_code': 200
    }, status=status.HTTP_200_OK)
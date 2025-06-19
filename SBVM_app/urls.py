from django.urls import path
from .views import (
    get_all_students,
    add_student,
    student_detail,
    student_login,
    student_logout
)

urlpatterns = [
    path('students/', get_all_students),
    path('students/add/', add_student),  
    path('students/<int:id>/', student_detail),
    path('students/login/', student_login), 
    path('students/logout/', student_logout),
]

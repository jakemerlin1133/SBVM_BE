from django.contrib import admin
from .models import Student

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'password', 'first_name', 'last_name', 'bottle_count', 'created_at')
    search_fields = ('student_id', 'first_name', 'last_name')
    list_filter = ('created_at',)

admin.site.register(Student, StudentAdmin)
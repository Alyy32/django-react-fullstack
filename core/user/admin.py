from django.contrib import admin
from .models import Student, Parent, Instructor, UserProfile


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'occupation', 'created_at']
    list_filter = ['created_at', 'occupation']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'grade_level', 'gpa', 'major', 'enrollment_date']
    list_filter = ['grade_level', 'enrollment_date', 'major']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'student_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'specialization', 'years_experience']
    list_filter = ['department', 'specialization', 'hire_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']
    readonly_fields = ['created_at', 'updated_at']


# Register UserProfile for backward compatibility
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'occupation', 'created_at']
    list_filter = ['created_at', 'occupation']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']

from django.contrib.auth import get_user_model  # pylint: disable=imported-auth-user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, Parent, Student, Instructor

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile
    """
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile': {
                    'phone_number': profile.phone_number,
                    'birth_date': profile.birth_date,
                    'bio': profile.bio,
                    'avatar': profile.avatar
                }
            }
        }, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        UserProfile.objects.create(user=user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile': {
                    'phone_number': '',
                    'birth_date': None,
                    'bio': '',
                    'avatar': ''
                }
            }
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def simple_user_demo(request):
    """
    Simple demonstration endpoint using URL patterns (not routers)
    Shows how to work with user data
    """
    user_count = User.objects.count()
    profile_count = UserProfile.objects.count()
    
    return Response({
        'message': 'Simple user model demonstration',
        'url_pattern': 'path("users/", views.simple_user_demo)',
        'explanation': 'This uses Django URL patterns, not DRF routers',
        'statistics': {
            'total_users': user_count,
            'user_profiles': profile_count
        },
        'note': 'Simple and clean - exactly what you needed!'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def students_list(request):
    """
    Get list of all students
    """
    students = Student.objects.all()
    students_data = []
    
    for student in students:
        students_data.append({
            'id': student.id,
            'user': {
                'username': student.user.username,
                'first_name': student.user.first_name,
                'last_name': student.user.last_name,
                'email': student.user.email,
            },
            'student_id': student.student_id,
            'grade_level': student.grade_level,
            'gpa': str(student.gpa) if student.gpa else None,
            'major': student.major,
            'enrollment_date': student.enrollment_date,
        })
    
    return Response({
        'students': students_data,
        'count': len(students_data)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def parents_list(request):
    """
    Get list of all parents
    """
    parents = Parent.objects.all()
    parents_data = []
    
    for parent in parents:
        parents_data.append({
            'id': parent.id,
            'user': {
                'username': parent.user.username,
                'first_name': parent.user.first_name,
                'last_name': parent.user.last_name,
                'email': parent.user.email,
            },
            'phone_number': parent.phone_number,
            'occupation': parent.occupation,
            'address': parent.address,
            'children_count': parent.children.count() if hasattr(parent, 'children') else 0,
        })
    
    return Response({
        'parents': parents_data,
        'count': len(parents_data)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instructors_list(request):
    """
    Get list of all instructors
    """
    instructors = Instructor.objects.all()
    instructors_data = []
    
    for instructor in instructors:
        instructors_data.append({
            'id': instructor.id,
            'user': {
                'username': instructor.user.username,
                'first_name': instructor.user.first_name,
                'last_name': instructor.user.last_name,
                'email': instructor.user.email,
            },
            'employee_id': instructor.employee_id,
            'department': instructor.department,
            'specialization': instructor.specialization,
            'office_location': instructor.office_location,
            'years_experience': instructor.years_experience,
        })
    
    return Response({
        'instructors': instructors_data,
        'count': len(instructors_data)
    }, status=status.HTTP_200_OK)

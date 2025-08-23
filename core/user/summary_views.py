from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model  # pylint: disable=imported-auth-user

from core.user.models import Student, Parent, Instructor, UserProfile

User = get_user_model()


@api_view(['GET'])
def user_models_summary(request):
    """
    Summary endpoint showing the new user models structure
    """
    return Response({
        'message': 'User Models Package Structure',
        'structure': {
            'core/user/models/': {
                '__init__.py': 'Package initialization with all model imports',
                'student.py': 'Student model with academic fields',
                'parent.py': 'Parent model with guardian information',
                'instructor.py': 'Instructor model with teaching details'
            }
        },
        'available_models': [
            'Student',
            'Parent', 
            'Instructor',
            'UserProfile (backward compatibility)'
        ],
        'statistics': {
            'total_users': User.objects.count(),
            'students': Student.objects.count(),
            'parents': Parent.objects.count(),
            'instructors': Instructor.objects.count(),
            'user_profiles': UserProfile.objects.count(),
        },
        'endpoints': {
            '/api/user/students/': 'List all students',
            '/api/user/parents/': 'List all parents',
            '/api/user/instructors/': 'List all instructors',
            '/api/user/profile/': 'Current user profile',
            '/api/user/demo/': 'Demo endpoint',
            '/api/user/summary/': 'This summary endpoint'
        }
    }, status=status.HTTP_200_OK)

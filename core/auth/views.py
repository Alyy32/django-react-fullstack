from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()  # pylint: disable=invalid-name


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def signin(request):
    """
    Handle user sign in
    """
    if request.method == 'GET':
        return Response({
            'message': 'Sign in endpoint',
            'required_fields': ['username', 'password']
        })
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({
            'message': 'Sign in successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Handle user registration
    """
    if request.method == 'GET':
        return Response({
            'message': 'Sign up endpoint',
            'required_fields': ['username', 'email', 'password']
        })
    
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    if not username or not email or not password:
        return Response({
            'error': 'Username, email, and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({
            'error': 'Username already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({
            'error': 'Email already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
        first_name=first_name,
        last_name=last_name
    )
    
    return Response({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signout(request):
    """
    Handle user sign out
    """
    logout(request)
    return Response({
        'message': 'Signed out successfully'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Handle password reset request
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # In a production environment, you would implement email sending logic here
    # For now, we return a success message regardless of whether the email exists
    # This prevents email enumeration attacks
    return Response({
        'message': 'If this email is registered, you will receive a password reset link'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Handle password change
    """
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not current_password or not new_password:
        return Response({
            'error': 'Current password and new password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    if not user.check_password(current_password):
        return Response({
            'error': 'Current password is incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({
        'message': 'Password changed successfully'
    })

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from .models import UserProfile
from .redis_utils import RedisHelper, cache_get, cache_set

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def hello_world(request):
    """
    Simple hello world endpoint
    """
    return Response({
        'message': 'Hello from Django backend!',
        'status': 'success',
        'timestamp': '2025-08-20'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """
    API status check endpoint
    """
    return Response({
        'status': 'API is running successfully',
        'version': '1.0.0',
        'django_version': '5.0.7'
    }, status=status.HTTP_200_OK)

# Authentication endpoints
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    Simple user login endpoint
    """
    if request.method == 'GET':
        return Response({
            'message': 'Login endpoint - use POST with username/email and password'
        })
    
    try:
        data = json.loads(request.body)
        username_or_email = data.get('username') or data.get('email')
        password = data.get('password')
        
        if not username_or_email or not password:
            return Response({
                'error': 'Username/email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to authenticate
        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON data'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_signup(request):
    """
    Simple user registration endpoint
    """
    if request.method == 'GET':
        return Response({
            'message': 'Signup endpoint - use POST with name, email, and password'
        })
    
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not name or not email or not password:
            return Response({
                'error': 'Name, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'User with this email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create username from email
        username = email.split('@')[0]
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        
        # Split name
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
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
        
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Simple user logout endpoint
    """
    logout(request)
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)

# Simple endpoint demonstrating URL patterns (not routers)
@api_view(['GET'])
@permission_classes([AllowAny])
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


# Redis demonstration endpoints
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def redis_demo(request):
    """
    Redis demonstration endpoint - shows caching functionality
    """
    if request.method == 'GET':
        # Try to get cached data first
        cached_data = cache_get('demo_data')
        
        if cached_data:
            return Response({
                'message': 'Data retrieved from Redis cache!',
                'source': 'Redis Cache',
                'cached_data': cached_data,
                'cache_hit': True,
                'url_pattern': 'path("redis/", views.redis_demo)',
                'explanation': 'This data was served from Redis cache (much faster!)'
            }, status=status.HTTP_200_OK)
        else:
            # Simulate expensive operation (database query, API call, etc.)
            demo_data = {
                'timestamp': datetime.now().isoformat(),
                'message': 'This is expensive data that should be cached',
                'computation_result': sum(range(1000)),  # Simulate calculation
                'user_count': User.objects.count()
            }
            
            # Cache the data for 5 minutes
            cache_set('demo_data', demo_data, 300)
            
            return Response({
                'message': 'Data computed and stored in Redis cache',
                'source': 'Fresh Computation',
                'data': demo_data,
                'cache_hit': False,
                'url_pattern': 'path("redis/", views.redis_demo)',
                'explanation': 'This data was computed fresh and stored in Redis for next time'
            }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            key = data.get('key', 'custom_data')
            value = data.get('value', 'default_value')
            timeout = data.get('timeout', 300)
            
            # Store in Redis
            cache_set(key, value, timeout)
            
            return Response({
                'message': f'Data stored in Redis with key: {key}',
                'key': key,
                'value': value,
                'timeout': timeout,
                'url_pattern': 'path("redis/", views.redis_demo)',
                'method': 'POST'
            }, status=status.HTTP_201_CREATED)
            
        except json.JSONDecodeError:
            return Response({
                'error': 'Invalid JSON data'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def redis_stats(request):
    """
    Show Redis cache statistics and status
    """
    stats = RedisHelper.get_cache_stats()
    
    # Try to get some sample cached keys
    sample_data = {
        'demo_data': cache_get('demo_data'),
        'custom_data': cache_get('custom_data'),
    }
    
    return Response({
        'message': 'Redis cache statistics',
        'cache_stats': stats,
        'sample_cached_data': sample_data,
        'cache_examples': {
            'set_data': 'POST /api/redis/ with {"key": "mykey", "value": "myvalue"}',
            'get_data': 'GET /api/redis/ (automatically caches demo data)',
            'clear_cache': 'DELETE /api/redis/clear/'
        },
        'url_pattern': 'path("redis/stats/", views.redis_stats)',
        'explanation': 'Redis is great for caching, sessions, and fast data storage!'
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def redis_clear(request):
    """
    Clear specific cache keys for cache management
    """
    keys_to_clear = ['demo_data', 'custom_data']
    cleared_keys = []
    
    for key in keys_to_clear:
        if cache_get(key) is not None:
            RedisHelper.delete_cache(key)
            cleared_keys.append(key)
    
    return Response({
        'message': f'Cleared {len(cleared_keys)} cache keys',
        'cleared_keys': cleared_keys,
        'url_pattern': 'path("redis/clear/", views.redis_clear)',
        'method': 'DELETE'
    }, status=status.HTTP_200_OK)

from django.contrib.auth import get_user_model  # pylint: disable=imported-auth-user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from core.redis_utils import RedisHelper, cache_get, cache_set

User = get_user_model()

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
            # Handle empty request body
            if not request.body:
                return Response({
                    'error': 'Request body cannot be empty'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            data = json.loads(request.body)
            key = data.get('key', 'custom_data')
            value = data.get('value', 'default_value')
            timeout = data.get('timeout', 300)
            
            # Validate inputs
            if not isinstance(key, str) or len(key.strip()) == 0:
                return Response({
                    'error': 'Key must be a non-empty string'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if not isinstance(timeout, int) or timeout <= 0:
                return Response({
                    'error': 'Timeout must be a positive integer'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Store in Redis
            cache_set(key.strip(), value, timeout)
            
            return Response({
                'message': f'Data stored in Redis with key: {key}',
                'key': key.strip(),
                'value': value,
                'timeout': timeout,
                'url_pattern': 'path("redis/", views.redis_demo)',
                'method': 'POST'
            }, status=status.HTTP_201_CREATED)
            
        except json.JSONDecodeError:
            return Response({
                'error': 'Invalid JSON data'
            }, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError) as e:
            return Response({
                'error': f'An error occurred while storing data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def redis_stats(request):
    """
    Show Redis cache statistics and status
    """
    try:
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
        
    except (ConnectionError, TimeoutError, AttributeError) as e:
        return Response({
            'error': f'Failed to retrieve Redis statistics: {str(e)}',
            'cache_stats': {'status': 'Error'},
            'url_pattern': 'path("redis/stats/", views.redis_stats)'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def redis_clear(request):
    """
    Clear specific cache keys for cache management
    """
    try:
        keys_to_clear = ['demo_data', 'custom_data', 'teacher_demo']
        cleared_keys = []
        failed_keys = []
        
        for key in keys_to_clear:
            try:
                if cache_get(key) is not None:
                    success = RedisHelper.delete_cache(key)
                    if success:
                        cleared_keys.append(key)
                    else:
                        failed_keys.append(key)
            except (ConnectionError, TimeoutError, AttributeError) as e:
                failed_keys.append(f"{key} (Error: {str(e)})")
        
        response_data = {
            'message': f'Cleared {len(cleared_keys)} cache keys',
            'cleared_keys': cleared_keys,
            'url_pattern': 'path("redis/clear/", views.redis_clear)',
            'method': 'DELETE'
        }
        
        if failed_keys:
            response_data['failed_keys'] = failed_keys
            response_data['warning'] = f'Failed to clear {len(failed_keys)} keys'
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except (ConnectionError, TimeoutError, AttributeError) as e:
        return Response({
            'error': f'Failed to clear cache: {str(e)}',
            'url_pattern': 'path("redis/clear/", views.redis_clear)',
            'method': 'DELETE'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

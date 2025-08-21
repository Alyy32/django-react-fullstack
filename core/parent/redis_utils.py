"""
Redis utilities for caching and data storage
"""
from django.core.cache import cache
from django.conf import settings
import json
from datetime import datetime, timedelta

class RedisHelper:
    """
    Simple Redis helper class for common operations
    """
    
    @staticmethod
    def set_cache(key, value, timeout=None):
        """
        Set a value in cache with optional timeout
        """
        if timeout is None:
            timeout = getattr(settings, 'CACHE_TTL', 300)
        
        return cache.set(key, value, timeout)
    
    @staticmethod
    def get_cache(key, default=None):
        """
        Get a value from cache
        """
        return cache.get(key, default)
    
    @staticmethod
    def delete_cache(key):
        """
        Delete a key from cache
        """
        return cache.delete(key)
    
    @staticmethod
    def set_user_session_data(user_id, data, timeout=3600):
        """
        Store user session data in Redis
        """
        key = f"user_session_{user_id}"
        return cache.set(key, data, timeout)
    
    @staticmethod
    def get_user_session_data(user_id):
        """
        Get user session data from Redis
        """
        key = f"user_session_{user_id}"
        return cache.get(key)
    
    @staticmethod
    def cache_api_response(endpoint, response_data, timeout=300):
        """
        Cache API response for faster subsequent requests
        """
        key = f"api_cache_{endpoint.replace('/', '_')}"
        cache_data = {
            'data': response_data,
            'cached_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=timeout)).isoformat()
        }
        return cache.set(key, cache_data, timeout)
    
    @staticmethod
    def get_cached_api_response(endpoint):
        """
        Get cached API response
        """
        key = f"api_cache_{endpoint.replace('/', '_')}"
        return cache.get(key)
    
    @staticmethod
    def increment_counter(key, amount=1):
        """
        Increment a counter in Redis (useful for API rate limiting, etc.)
        """
        try:
            return cache.get_or_set(key, 0) + amount
        except:
            cache.set(key, amount, 3600)  # 1 hour default
            return amount
    
    @staticmethod
    def get_cache_stats():
        """
        Get basic cache statistics (if available)
        """
        try:
            # This is a simplified version - in real Redis you'd use INFO command
            return {
                'cache_backend': 'Redis',
                'cache_location': getattr(settings, 'CACHES', {}).get('default', {}).get('LOCATION', 'Unknown'),
                'status': 'Connected'
            }
        except:
            return {
                'cache_backend': 'Redis',
                'status': 'Error'
            }

# Quick access functions
def cache_set(key, value, timeout=None):
    """Quick cache set function"""
    return RedisHelper.set_cache(key, value, timeout)

def cache_get(key, default=None):
    """Quick cache get function"""
    return RedisHelper.get_cache(key, default)

def cache_delete(key):
    """Quick cache delete function"""
    return RedisHelper.delete_cache(key)

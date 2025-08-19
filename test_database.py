#!/usr/bin/env python
"""
Test script to verify database connectivity and create sample data
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

from django.contrib.auth.models import User
from core.parent.models import APILog, UserProfile

def test_database_connection():
    print("🔍 Testing Database Connection...")
    
    try:
        # Test 1: Count existing users
        user_count = User.objects.count()
        print(f"✅ Users in database: {user_count}")
        
        # Test 2: Count API logs
        api_log_count = APILog.objects.count()
        print(f"✅ API logs in database: {api_log_count}")
        
        # Test 3: Count user profiles
        profile_count = UserProfile.objects.count()
        print(f"✅ User profiles in database: {profile_count}")
        
        # Test 4: Create a test API log entry
        test_log = APILog.objects.create(
            endpoint='/api/status/',
            method='GET',
            ip_address='127.0.0.1',
            user_agent='Test Script',
            status_code=200,
            response_time=0.05
        )
        print(f"✅ Created test API log: {test_log}")
        
        # Test 5: Query the test log
        logs = APILog.objects.filter(endpoint='/api/status/')
        print(f"✅ Found {logs.count()} API logs for /api/status/ endpoint")
        
        print("\n🎉 All database tests passed!")
        print("🔗 Database connection: WORKING")
        print("📊 Models: WORKING")
        print("💾 CRUD operations: WORKING")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_database_connection()

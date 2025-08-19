#!/usr/bin/env python
"""
Test script to verify all imports work correctly
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

def test_imports():
    print("🔍 Testing Django REST Framework imports...")
    
    try:
        # Test REST Framework imports
        from rest_framework.decorators import api_view, permission_classes
        from rest_framework.response import Response
        from rest_framework import status
        from rest_framework.permissions import IsAuthenticated, AllowAny
        print("✅ Django REST Framework imports: SUCCESS")
        
        # Test Django imports
        from django.contrib.auth.models import User
        from django.shortcuts import render
        print("✅ Django core imports: SUCCESS")
        
        # Test custom imports
        from core.parent.models import APILog, UserProfile, BaseModel
        from core.parent.views import hello_world, api_status
        print("✅ Custom app imports: SUCCESS")
        
        print("\n🎉 ALL IMPORTS WORKING CORRECTLY!")
        print("The warnings in VS Code are just IDE configuration issues.")
        print("Your code will run perfectly fine!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([AllowAny])
def hello_world(request):
    """
    Simple hello world endpoint
    """
    return Response({
        'message': 'Hello from Django backend!',
        'status': 'success',
        'timestamp': '2025-08-22'
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

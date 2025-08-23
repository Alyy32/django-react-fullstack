"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.authentication.urls')),
    path('api/user/', include('core.user.urls')),
    path('api/redis/', include('core.redis_demo.urls')),
    path('api/hello/', api_views.hello_world, name='hello_world'),
    path('api/status/', api_views.api_status, name='api_status'),
]

from django.urls import path
from . import views

urlpatterns = [
    # Basic API endpoints
    path('hello/', views.hello_world, name='hello_world'),
    path('hello', views.hello_world, name='hello_world_no_slash'),
    path('status/', views.api_status, name='api_status'),
    path('status', views.api_status, name='api_status_no_slash'),
    
    # Simple user demonstration endpoint (URL patterns, not routers)
    path('users/', views.simple_user_demo, name='simple_user_demo'),
    path('users', views.simple_user_demo, name='simple_user_demo_no_slash'),
    
    # Authentication endpoints
    path('auth/login/', views.user_login, name='user_login'),
    path('auth/login', views.user_login, name='user_login_no_slash'),
    path('auth/signup/', views.user_signup, name='user_signup'),
    path('auth/signup', views.user_signup, name='user_signup_no_slash'),
    path('auth/logout/', views.user_logout, name='user_logout'),
    path('auth/logout', views.user_logout, name='user_logout_no_slash'),
    path('auth/profile/', views.user_profile, name='user_profile'),
    path('auth/profile', views.user_profile, name='user_profile_no_slash'),
    

    path('redis/', views.redis_demo, name='redis_demo'),
    path('redis', views.redis_demo, name='redis_demo_no_slash'),
    path('redis/stats/', views.redis_stats, name='redis_stats'),
    path('redis/stats', views.redis_stats, name='redis_stats_no_slash'),
    path('redis/clear/', views.redis_clear, name='redis_clear'),
    path('redis/clear', views.redis_clear, name='redis_clear_no_slash'),
]



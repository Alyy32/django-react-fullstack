from django.urls import path
from . import views

urlpatterns = [
    # API endpoints (with and without trailing slashes)
    path('hello/', views.hello_world, name='hello_world'),
    path('hello', views.hello_world, name='hello_world_no_slash'),
    path('status/', views.api_status, name='api_status'),
    path('status', views.api_status, name='api_status_no_slash'),
    
    # Authentication endpoints (with and without trailing slashes)
    path('auth/login/', views.user_login, name='user_login'),
    path('auth/login', views.user_login, name='user_login_no_slash'),
    path('auth/signup/', views.user_signup, name='user_signup'),
    path('auth/signup', views.user_signup, name='user_signup_no_slash'),
    path('auth/logout/', views.user_logout, name='user_logout'),
    path('auth/logout', views.user_logout, name='user_logout_no_slash'),
    path('auth/profile/', views.user_profile, name='user_profile'),
    path('auth/profile', views.user_profile, name='user_profile_no_slash'),
    path('auth/forgot-password/', views.forgot_password, name='forgot_password'),
    path('auth/forgot-password', views.forgot_password, name='forgot_password_no_slash'),
]

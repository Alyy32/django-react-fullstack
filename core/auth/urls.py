from django.urls import path
from core.auth import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change-password/', views.change_password, name='change_password'),
]

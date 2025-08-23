from django.urls import path
from . import views

urlpatterns = [
    path('', views.redis_demo, name='redis_demo'),
    path('stats/', views.redis_stats, name='redis_stats'),
    path('clear/', views.redis_clear, name='redis_clear'),
]

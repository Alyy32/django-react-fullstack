from django.urls import path
from . import views
from . import summary_views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('demo/', views.simple_user_demo, name='simple_user_demo'),
    path('students/', views.students_list, name='students_list'),
    path('parents/', views.parents_list, name='parents_list'),
    path('instructors/', views.instructors_list, name='instructors_list'),
    path('summary/', summary_views.user_models_summary, name='user_models_summary'),
]

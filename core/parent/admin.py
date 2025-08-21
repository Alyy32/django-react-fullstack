from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Simple admin interface for User Profiles
    """
    list_display = ['user', 'phone_number', 'birth_date', 'created_at']
    list_filter = ['created_at', 'updated_at', 'birth_date']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('phone_number', 'birth_date', 'bio', 'avatar')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Simple and clean admin - no complex inlines or custom methods needed!

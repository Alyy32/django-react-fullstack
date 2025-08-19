from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import APILog, UserProfile

# Customize the User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 0

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    inlines = (UserProfileInline,)
    
    readonly_fields = ('last_login', 'date_joined')

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'method', 'status_code', 'user', 'ip_address', 'response_time', 'created_at')
    list_filter = ('method', 'status_code', 'created_at', 'is_active')
    search_fields = ('endpoint', 'user__username', 'ip_address')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Request Info', {
            'fields': ('endpoint', 'method', 'status_code', 'user', 'ip_address')
        }),
        ('Technical Details', {
            'fields': ('user_agent', 'response_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'birth_date', 'created_at')
    list_filter = ('created_at', 'is_active')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Personal Details', {
            'fields': ('phone_number', 'birth_date', 'bio', 'avatar')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site headers
admin.site.site_header = "Wisecool Admin Dashboard"
admin.site.site_title = "Wisecool Admin"
admin.site.index_title = "Welcome to Wisecool Administration"

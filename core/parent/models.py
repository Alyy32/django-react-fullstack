from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class APILog(BaseModel):
    """
    Model to track API usage and requests
    """
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    status_code = models.IntegerField()
    response_time = models.FloatField(help_text='Response time in seconds')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'API Log'
        verbose_name_plural = 'API Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code}"

class UserProfile(BaseModel):
    """
    Extended user profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.URLField(blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

from datetime import date

from django.contrib.auth import get_user_model  # pylint: disable=imported-auth-user
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    """
    Simple user profile model - exactly what you needed!
    Extends Django's built-in User model with additional fields
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.user.username}'s Profile"

    def get_full_name(self):
        """Return the user's full name"""
        # pylint: disable=no-member
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @property
    def age(self):
        """Return the user's age in years"""
        if not self.birth_date:
            return None

        today = date.today()
        # pylint: disable=no-member
        born = self.birth_date
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return age

    def clean(self):
        """Validate the model"""
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError('Birth date cannot be in the future.')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

# That's it! Simple and clean user model with proper validation.
# You can use Django's built-in User model for authentication
# and this UserProfile for additional user information.

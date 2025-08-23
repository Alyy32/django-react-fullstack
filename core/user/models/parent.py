from datetime import date

from django.contrib.auth import get_user_model  # pylint: disable=imported-auth-user
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Parent(models.Model):
    """
    Parent model for managing parent/guardian information
    Extends Django's built-in User model with parent-specific fields
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
    
    # Parent-specific fields
    occupation = models.CharField(max_length=100, blank=True)
    emergency_contact = models.CharField(max_length=17, blank=True)
    address = models.TextField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.user.username} (Parent)"

    def get_full_name(self):
        """Return the parent's full name"""
        # pylint: disable=no-member
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @property
    def age(self):
        """Return the parent's age in years"""
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
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'


# Keep the original UserProfile for backward compatibility
class UserProfile(Parent):
    """
    Backward compatibility alias for Parent model
    """
    class Meta:
        proxy = True
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

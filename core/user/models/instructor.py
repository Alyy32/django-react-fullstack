from datetime import date

from django.contrib.auth import get_user_model  # pylint: disable=imported-auth-user
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Instructor(models.Model):
    """
    Instructor model for managing instructor/teacher information
    Extends Django's built-in User model with instructor-specific fields
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
    
    # Instructor-specific fields
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    hire_date = models.DateField(default=date.today)
    office_location = models.CharField(max_length=100, blank=True)
    office_hours = models.TextField(max_length=200, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    years_experience = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.user.username} (Instructor - ID: {self.employee_id})"

    def get_full_name(self):
        """Return the instructor's full name"""
        # pylint: disable=no-member
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @property
    def age(self):
        """Return the instructor's age in years"""
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
        
        if self.years_experience < 0:
            raise ValidationError('Years of experience cannot be negative.')

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'
        ordering = ['employee_id']

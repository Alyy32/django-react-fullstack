from datetime import date

from django.contrib.auth import get_user_model  # pylint: disable=imported-auth-user
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Student(models.Model):
    """
    Student model for managing student information
    Extends Django's built-in User model with student-specific fields
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
    
    # Student-specific fields
    student_id = models.CharField(max_length=20, unique=True)
    grade_level = models.CharField(max_length=20, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)  # Changed from default=date.today
    graduation_year = models.IntegerField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    
    # Parent relationship (simplified reference)
    parent = models.ForeignKey(
        'Parent', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='children'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.user.username} (Student - ID: {self.student_id})"

    def get_full_name(self):
        """Return the student's full name"""
        # pylint: disable=no-member
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @property
    def age(self):
        """Return the student's age in years"""
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
        
        if self.gpa and (self.gpa < 0 or self.gpa > 4.0):
            raise ValidationError('GPA must be between 0.0 and 4.0.')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['student_id']

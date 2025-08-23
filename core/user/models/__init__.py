# Import all models to make them available from the package
from .student import Student
from .parent import Parent, UserProfile
from .instructor import Instructor

__all__ = [
    'Student',
    'Parent', 
    'Instructor',
    'UserProfile',
]

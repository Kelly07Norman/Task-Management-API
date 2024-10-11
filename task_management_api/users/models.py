from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model that extends Django's built-in AbstractUser.

    This class extends the default user model to include a unique email field, 
    allowing for flexibility in future expansions such as adding more fields or methods.
    
    """
    email = models.EmailField(unique=True)  # Email must be unique

    def __str__(self):
        return self.username  # Return the username for easy identification
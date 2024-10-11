from django.db import models
from users.models import User

class TaskCategory(models.Model):
    """
    TaskCategory model to categorize tasks.

    Attributes:
        name (str): The name of the task category.
        user (ForeignKey): The user associated with this category.
    """
    name = models.CharField(max_length=100, unique=True)  # Category name must be unique
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')  # Link to the user

    def __str__(self):
        return self.name  # String representation of the category

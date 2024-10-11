from django.db import models
from users.models import User  # Importing the User model
from categories.models import TaskCategory  # Importing the TaskCategory model

# Defining the Task model 
class Task(models.Model):
    """
    Model representing a task assigned to a user. 
    Each task is associated with a category and has attributes for title, description, 
    due date, priority, status, and completion.
    """

    # Priority levels for tasks
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    # Choices for priority field
    PRIORITY_LEVELS = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    # Status choices for tasks
    PENDING = 'Pending'
    COMPLETED = 'Completed'

    # Choices for status field
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]

    # Task attributes
    title = models.CharField(max_length=255)  # The title of the task
    description = models.TextField()  # Detailed description of the task
    due_date = models.DateTimeField()  # Date and time the task is due
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default=MEDIUM)  # Priority level with default as 'Medium'
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)  # Status of the task (Pending/Completed)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when task is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when task is updated
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who owns the task
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)  # Task category (linked to TaskCategory model)
    is_completed = models.BooleanField(default=False)  # Boolean to track if the task is completed

    def __str__(self):
        """
        Return the string representation of the task.
        """
        return self.title  # Return the task title for easy identification

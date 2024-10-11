from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Task, TaskCategory  # Import the Task model
from .serializers import TaskSerializer  # Import the Task serializer
from django.core.exceptions import ValidationError

# Admin View for List of All Tasks
class AdminTaskListView(generics.ListAPIView):
    """
    AdminTaskListView provides a read-only list of all tasks in the system.
    It is restricted to admin users only.
    """
    serializer_class = TaskSerializer  # Specify the serializer to use
    permission_classes = [permissions.IsAdminUser]  # Require admin permissions

    def get_queryset(self):
        # Return all tasks regardless of the user
        return Task.objects.all()

# Admin Delete All Tasks View
class AdminDeleteAllTasksView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]  # Only allow admin users

    def delete(self, request, *args, **kwargs):
        """
        Delete all tasks in the database.
        """
        deleted_count, _ = Task.objects.all().delete()  # Delete all tasks and get the count
        return Response({
            "message": f"Successfully deleted {deleted_count} tasks."
        }, status=status.HTTP_204_NO_CONTENT)

# Task List View (Retrieve all tasks for authenticated user)
class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer  # Specify the serializer to use
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        # Return only tasks that belong to the authenticated user
        return Task.objects.filter(user=self.request.user)  # Filter by 'user'
    
    def perform_create(self, serializer):
        # Assign the authenticated user as the task's owner
        serializer.save(user=self.request.user)  # Set 'user' field

# Task Detail View (Retrieve, Update, Delete a specific task)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer  # Specify the serializer to use
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        # Return only tasks that belong to the authenticated user
        return Task.objects.filter(user=self.request.user)  # Filter by 'user'

    def delete(self, request, *args, **kwargs):
        """Override delete method to provide custom response."""
        task = self.get_object()  # Get the task object
        task_title = task.title  # Capture task title or other info you want in the message
        task.delete()  # Delete the task
    
        # Return a custom response message with a status
        return Response({
            "message": f"Task '{task_title}' has been successfully deleted."
        }, status=status.HTTP_200_OK)

# Task Completion Toggle View (Mark a task as complete)
class TaskToggleCompleteView(generics.UpdateAPIView):
    serializer_class = TaskSerializer  # Specify the serializer to use
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        # Return only tasks that belong to the authenticated user
        return Task.objects.filter(user=self.request.user)  # Filter by 'user'

    def patch(self, request, *args, **kwargs):
        task = self.get_object()  # Get the task instance
        print(f"Toggling task: {task.title} - Current status: {task.is_completed}")

        # Toggle the is_completed status
        task.is_completed = not task.is_completed
        task.status = 'Completed' if task.is_completed else 'Pending'  # Update the status based on completion
        task.save()

        # Return the updated task with completion status
        return Response({"id": task.id, "is_completed": task.is_completed, "status": task.status}, status=status.HTTP_200_OK)

# Task Incomplete Toggle View (Mark a task as incomplete)
class TaskToggleIncompleteView(generics.UpdateAPIView):
    serializer_class = TaskSerializer  # Specify the serializer to use
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        # Return only tasks that belong to the authenticated user
        return Task.objects.filter(user=self.request.user)  # Filter by 'user'

    def patch(self, request, *args, **kwargs):
        task = self.get_object()  # Get the task instance
        print(f"Marking task as incomplete: {task.title}")

        # Ensure the task is marked as incomplete
        task.is_completed = False
        task.status = 'Pending'  # Set status back to Pending
        task.save()

        # Return the updated task
        return Response({"id": task.id, "is_completed": task.is_completed, "status": task.status}, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        """Handle exceptions in a consistent way."""
        if isinstance(exc, Task.DoesNotExist):
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

# Task filter and sorting view
class TaskFilterView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        category = self.request.query_params.get('category')
        due_date = self.request.query_params.get('due_date')
        sort_by = self.request.query_params.get('sort_by')
        is_completed = self.request.query_params.get('is_completed')

        try:
            if status:
                if status not in ['Pending', 'Completed']:
                    raise ValidationError("Invalid status. Must be either 'Pending' or 'Completed'.")
                queryset = queryset.filter(status=status)

            if priority:
                if priority not in ['Low', 'Medium', 'High']:
                    raise ValidationError("Invalid priority. Must be 'Low', 'Medium', or 'High'.")
                queryset = queryset.filter(priority=priority)

            if due_date:
                queryset = queryset.filter(due_date__date=due_date)

            if category:
                # Check if the category exists and belongs to the user
                user_categories = TaskCategory.objects.filter(user=self.request.user).values_list('name', flat=True)
                if category not in user_categories:
                    raise ValidationError(f"Category '{category}' does not exist or does not belong to you.")
                queryset = queryset.filter(category__name=category)


            if is_completed is not None:
                is_completed = is_completed.lower() == 'true'
                queryset = queryset.filter(is_completed=is_completed)

            if sort_by:
                if sort_by not in ['due_date', 'priority', 'created_at', 'updated_at']:
                    raise ValidationError("Invalid sorting parameter. Must be 'due_date', 'priority', 'created_at', or 'updated_at'.")
                queryset = queryset.order_by(sort_by)

        except ValidationError as e:
            self.validation_error = str(e)
            return Task.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if hasattr(self, 'validation_error'):
            return Response({"error": self.validation_error}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
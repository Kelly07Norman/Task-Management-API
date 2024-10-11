from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import TaskCategory
from .serializers import CategorySerializer 

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def get_queryset(self):
        """
        Filter categories to return only those belonging to the authenticated user.
        """
        return TaskCategory.objects.filter(user=self.request.user)  # Filter by user

    def perform_create(self, serializer):
        """
        Automatically set the user to the currently authenticated user
        when a category is created.
        """
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Update a category instance.
        """
        instance = self.get_object()  # Get the category instance
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to edit this category."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Allow partial updates
        serializer.is_valid(raise_exception=True)  # Validate data
        self.perform_update(serializer)  # Save changes
        return Response(serializer.data)  # Return the updated category data

    def destroy(self, request, *args, **kwargs):
        """
        Delete a category instance.
        """
        instance = self.get_object()  # Get the category instance
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to delete this category."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)  # Delete the instance
        # Return a success message after deletion
        return Response({"message": f"Category '{instance.name}' has been successfully deleted."}, status=status.HTTP_200_OK)
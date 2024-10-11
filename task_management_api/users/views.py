from rest_framework import generics, permissions, status
from .models import User  # Import the User model
from .serializers import UserSerializer  # Import the User serializer
from rest_framework.response import Response

# User Registration View (Create User)
class UserCreateView(generics.CreateAPIView):
    """
    API view to handle user registration.
    Allows anyone to create a new user.
    """
    serializer_class = UserSerializer  # Specify the serializer to use for user data
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

# User Profile View for Retrieving and Updating a User
class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update the authenticated user's profile.
    Requires the user to be authenticated.
    """
    queryset = User.objects.all()  # Get all users
    serializer_class = UserSerializer  
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get_queryset(self):
        """
        Limit the queryset to only the authenticated user's data.
        This prevents a user from accessing other users' data.
        """
        return self.queryset.filter(id=self.request.user.id)

# List Users View for Admin
class UserListView(generics.ListAPIView):
    """
    API view to list all users.
    Only admin users can access this view.
    """
    queryset = User.objects.all()  # Get all users
    serializer_class = UserSerializer 
    permission_classes = [permissions.IsAdminUser]  #Ensuring this view is only accessible to admin users

# User Deletion View (Delete a specific user)
class UserDeleteView(generics.DestroyAPIView):
    """
    API view to allow authenticated users to delete their own account.
    Admin users can delete any user's account.
    """
    queryset = User.objects.all()  # Get all users
    serializer_class = UserSerializer  
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        """
        Returns the appropriate queryset based on user role.
        Admins can see all users; regular users can only delete themselves.
        """
        if self.request.user.is_staff:
            return self.queryset  # Admin can see all users
        return self.queryset.filter(id=self.request.user.id)  # Regular user can only delete self

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a user.
        Logs the username of the deleted user for debugging or tracking.
        """
        user_deleted = instance.username
        instance.delete()  # Delete the user instance
        print(f"User '{user_deleted}' has been successfully deleted.")  # Message to display to user

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to return a custom success message.
        """
        response = super().delete(request, *args, **kwargs)  # Call parent's delete method
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)


# Admin Delete All Users View (Delete all users)
class AdminDeleteAllUsersView(generics.DestroyAPIView):
    """
    Admin-only view to delete all users in the system, except the superuser.
    """
    permission_classes = [permissions.IsAdminUser]  # Only admin users can perform this action

    def delete(self, request, *args, **kwargs):
        """
        Custom delete method to remove all users except the superuser.
        Returns a message with the number of deleted users.
        """
        deleted_count, _ = User.objects.filter(is_superuser=False).delete()  # Prevent deletion of superuser
        return Response({
            "message": f"Successfully deleted {deleted_count} users"
        }, status=status.HTTP_204_NO_CONTENT)
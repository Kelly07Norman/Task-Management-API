from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateView, UserDetailView, UserListView, UserDeleteView, AdminDeleteAllUsersView

urlpatterns = [
    # User registration
    path('users/register/', UserCreateView.as_view(), name='user-register'),  # POST: Register a new user

    # Login endpoint
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    
    # Token refresh endpoint
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    
    # User profile view
    path('users/profile/<int:pk>/', UserDetailView.as_view(), name='user-profile'), # GET: Retrieve user profile, PUT: Update user profile

    # Admin view for listing all users
    path('admin/users/', UserListView.as_view(), name='admin-user-list'),  # GET: List all users (admin only)

    # Delete a specific user (admin can delete anyone, regular users can delete themselves)
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),  # DELETE: Delete a specific user

    # Admin delete all users (excluding superuser)
    path('admin/users/delete/all/', AdminDeleteAllUsersView.as_view(), name='admin-delete-all-users'),  # DELETE: Delete all users (admin only)

   
]



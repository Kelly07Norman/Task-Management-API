from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

# Create a router for the API endpoints
router = DefaultRouter()
# Register the CategoryViewSet with the router
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),  # Include all router-generated URLs
]

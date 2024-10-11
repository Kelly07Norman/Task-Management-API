from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),  # Include task URLs
    path('api/', include('users.urls')),   # Include user URLs
    path('api/', include('categories.urls')),  # Include categories url
]

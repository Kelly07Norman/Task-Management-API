from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient  # Import APIClient
from users.models import User  # Ensure this points to your custom User model
from .models import Task

class TaskAPITest(APITestCase):
    def setUp(self):
        # Create a user using your custom User model
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Initialize the API client
        self.client = APIClient()
        
        # Authenticate the client
        self.client.force_authenticate(user=self.user)  # Force the authentication

    def test_create_task(self):
        url = reverse('task-list')  # Ensure this matches your URL patterns
        data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'due_date': '2024-10-01T12:00:00Z',  # Ensure this matches your expected format
            'priority': 'High',
            'status': 'Pending'
        }
        response = self.client.post(url, data)
        
        # Debugging: Print response status code and content for troubleshooting
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        
        # Assert that the response status code is HTTP 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')
from django.urls import path
from .views import (AdminTaskListView, AdminDeleteAllTasksView, TaskListView, TaskDetailView, TaskToggleCompleteView, TaskToggleIncompleteView, TaskFilterView)

urlpatterns = [
    # Admin views
    path('admin/tasks/', AdminTaskListView.as_view(), name='admin-task-list'),  # GET: List all tasks (admin only)
    path('admin/tasks/delete/all/', AdminDeleteAllTasksView.as_view(), name='admin-delete-all-tasks'),  # DELETE: Delete all tasks (admin only)

    # User views
    path('tasks/', TaskListView.as_view(), name='task-list'),  # GET: List user's tasks, POST: Create a new task
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),  # GET: Retrieve task, PUT: Update task, DELETE: Delete task
    
    # Task completion/incomplete toggle views
    path('tasks/<int:pk>/complete/', TaskToggleCompleteView.as_view(), name='task-toggle-complete'),  # PATCH: Toggle task completion
    path('tasks/<int:pk>/incomplete/', TaskToggleIncompleteView.as_view(), name='task-toggle-incomplete'),  # PATCH: Mark task as incomplete

    # Task filter and sorting view
    path('tasks/filter/', TaskFilterView.as_view(), name='task-filter'),  # GET: Filter and sort tasks
]

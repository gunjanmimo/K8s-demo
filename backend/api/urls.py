# --------------------------------DJANGO IMPORTS--------------------------------#
from django.urls import path

# ---------------------------------LOCAL IMPORTS---------------------------------#
from . import views

# URL patterns for the Image Processing API
urlpatterns = [
    # Endpoint for uploading an image
    path("apis/upload/", views.ImageUploadView.as_view(), name="upload"),
    # Endpoint for listing all image processing tasks
    path("apis/tasks/", views.ImageUploadView.as_view(), name="tasks"),
    # Endpoint for retrieving details of a specific task by ID
    path(
        "apis/tasks/<int:task_id>/", views.ImageUploadView.as_view(), name="task-detail"
    ),
    # frontend view
    path("", views.frontend_view, name="frontend"),
    # Debug endpoint for processing tasks manually (message queue debug)
    path(
        "apis/tasks/process/", views.ImageProcessingTaskView.as_view(), name="process"
    ),
]

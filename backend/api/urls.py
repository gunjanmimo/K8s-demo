from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.ImageUploadView.as_view(), name="upload"),
    path("tasks/", views.ImageUploadView.as_view(), name="tasks"),
    path("tasks/<int:task_id>/", views.ImageUploadView.as_view(), name="task-detail"),
    # message queue debug endpoint
    path("tasks/process/", views.ImageProcessingTaskView.as_view(), name="process"),
]

# --------------------------------PYTHON IMPORTS--------------------------------#
import os
import uuid

# --------------------------------DJANGO IMPORTS--------------------------------#
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

# ---------------------------------LOCAL IMPORTS---------------------------------#
from .models import ImageProcessingTask
from .serializers import ImageProcessingTaskSerializer
from message_queue import AzureImageMessageQueue


class ImageUploadView(APIView):
    """
    API View for handling image uploads and task management.
    """

    def __init__(self):
        self.queue_client = AzureImageMessageQueue()

    def post(self, request):
        """
        Handles the upload of an image file, performs sanity checks,
        stores the image, creates a processing task, and returns the task details.

        Args:
            request: The HTTP request object containing the image file.

        Returns:
            Response: JSON response containing the task details or an error message.
        """
        # STEP 1: Handle image upload
        file = request.FILES.get("image")

        # STEP 2: Sanity checks on file
        if not file:
            return Response(
                {"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check the content type of the uploaded file
        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            return Response(
                {"error": "Unsupported file type"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        # Generate a unique filename
        _, file_extension = os.path.splitext(file.name)
        filename = "original/" + f"{uuid.uuid4()}{file_extension}"

        # STEP 3: Create ImageProcessingTask record
        task = ImageProcessingTask.objects.create()

        # STEP 4: Store original image in cloud storage and push message to queue
        original_img_url = self.queue_client.push_message(
            file=file, file_name=filename, task_id=task.id
        )
        task.original_image_url = original_img_url
        task.save()

        # Serialize the task data and return the response
        serializer = ImageProcessingTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, task_id=None):
        """
        Retrieves the details of a specific image processing task or all tasks.

        Args:
            request: The HTTP request object.
            task_id (int, optional): The ID of the task to retrieve. Defaults to None.

        Returns:
            Response: JSON response containing the task details or an error message.
        """
        if task_id:
            try:
                task = ImageProcessingTask.objects.get(id=task_id)
                serializer = ImageProcessingTaskSerializer(task)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ImageProcessingTask.DoesNotExist:
                return Response(
                    {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            tasks = ImageProcessingTask.objects.all()
            serializer = ImageProcessingTaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ImageProcessingTaskView(APIView):
    """
    API View for handling image processing tasks.
    """

    def __init__(self):
        self.queue_client = AzureImageMessageQueue()

    def get(self, request):
        """
        Pulls messages from the queue to process image tasks.

        Args:
            request: The HTTP request object.

        Returns:
            Response: JSON response indicating the processing of image tasks.
        """
        self.queue_client.pull_message()
        return Response(
            {"message": "Processing image tasks"}, status=status.HTTP_200_OK
        )


def frontend_view(request):
    return render(request, "frontend.html")

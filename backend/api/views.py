# --------------------------------PYTHON IMPORTS--------------------------------#
import os
import uuid

# --------------------------------DJANGO IMPORTS--------------------------------#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# ---------------------------------LOCAL IMPORTS---------------------------------#
from .models import ImageProcessingTask
from .serializers import ImageProcessingTaskSerializer
from message_queue import AzureImageMessageQueue


class ImageUploadView(APIView):
    def __init__(self):
        # self.storage_client = AzureBlobStorage()
        self.queue_client = AzureImageMessageQueue()

    def post(self, request):

        # STEP 1. Handle image upload
        file = request.FILES.get("image")

        # STEP 2. Sanity checks on file
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

        # STEP 3: Create ImageTask record
        task = ImageProcessingTask.objects.create()

        # STEP 4: Store original image in cloud storage and push message to queue
        original_img_url = self.queue_client.push_message(
            file=file, file_name=filename, task_id=task.id
        )
        task.original_image_url = original_img_url
        task.save()

        serializer = ImageProcessingTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, task_id=None):
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
    def __init__(self):
        self.queue_client = AzureImageMessageQueue()

    def get(self, request):
        self.queue_client.pull_message()
        return Response(
            {"message": "Processing image tasks"}, status=status.HTTP_200_OK
        )

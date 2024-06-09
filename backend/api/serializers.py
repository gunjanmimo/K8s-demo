# --------------------------------DJANGO IMPORTS--------------------------------#
from rest_framework import serializers

# ---------------------------------LOCAL IMPORTS---------------------------------#
from .models import ImageProcessingTask


class ImageProcessingTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the ImageProcessingTask model.

    This serializer handles the conversion of ImageProcessingTask instances
    to and from JSON format, making it suitable for API responses and requests.

    Fields:
        original_image_url (str): URL of the original image.
        processed_image_url (str): URL of the processed image.
        status (str): Status of the image processing task, can be 'pending', 'processing', 'completed', or 'failed'.
        upload_time (datetime): Timestamp when the task was uploaded.
        processing_start_time (datetime): Timestamp when processing started.
        processing_end_time (datetime): Timestamp when processing ended.
    """

    class Meta:
        model = ImageProcessingTask
        fields = "__all__"

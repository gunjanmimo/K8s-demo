# --------------------------------DJANGO IMPORTS--------------------------------#
from django.db import models
from django.utils import timezone


class ImageProcessingTask(models.Model):
    """
    Model to represent an image processing task.

    Attributes:
        original_image_url (URLField): URL of the original image to be processed.
        processed_image_url (URLField): URL of the processed image.
        status (CharField): Current status of the processing task (e.g., pending, in_progress, completed).
        upload_time (DateTimeField): Timestamp when the image was uploaded.
        processing_start_time (DateTimeField): Timestamp when the processing started.
        processing_end_time (DateTimeField): Timestamp when the processing ended.
    """

    original_image_url = models.URLField(blank=True, null=True)
    processed_image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    upload_time = models.DateTimeField(auto_now_add=True)
    processing_start_time = models.DateTimeField(blank=True, null=True)
    processing_end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """
        String representation of the ImageProcessingTask model,
        which returns the URL of the original image.
        """
        return self.original_image_url

from django.db import models
from django.utils import timezone


class ImageProcessingTask(models.Model):
    original_image_url = models.URLField(blank=True, null=True)
    processed_image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    upload_time = models.DateTimeField(auto_now_add=True)
    processing_start_time = models.DateTimeField(blank=True, null=True)
    processing_end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.original_image_url

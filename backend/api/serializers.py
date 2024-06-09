from rest_framework import serializers
from .models import ImageProcessingTask


class ImageProcessingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProcessingTask
        fields = "__all__"

import time
from datetime import datetime
import requests
import json
import numpy as np
from azure.storage.queue import QueueServiceClient
from azure.storage.blob import BlobServiceClient
from django.conf import settings

# ------------------------------ LOCAL IMPORTS ------------------------------ #
from api.models import ImageProcessingTask
from storage import AzureBlobStorage
from image_processing import process_image


class AzureImageMessageQueue:
    def __init__(self):

        # initialize the blob storage client
        self.blob_storage = AzureBlobStorage()

        # initialize the queue client
        self.queue_service_client = QueueServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )
        self.queue_client = self.queue_service_client.get_queue_client(
            settings.AZURE_QUEUES_NAME
        )

    # push message to queue
    def push_message(self, file: bytes, file_name: str, task_id: int) -> str:
        try:
            image_url = self.blob_storage.upload_file(file=file, file_name=file_name)
            message_content = json.dumps(
                {
                    "task_id": task_id,
                }
            )
            self.queue_client.send_message(message_content)
            return image_url
        except Exception as e:
            raise

    def pull_message(self) -> None:
        messages = self.queue_client.receive_messages(max_messages=5)
        for msg_batch in messages.by_page():
            for msg in msg_batch:
                
                
                task_id = json.loads(msg.content)["task_id"]
                self.process_message(task_id)

                try:
                    self.queue_client.delete_message(msg.id, msg.pop_receipt)
                    print(f"Deleted message with ID: {msg.id}")
                except Exception as e:
                    print(f"Error deleting message: {e}")
                
    

        
    def process_message(self, task_id) -> bool:
        try:
            task = ImageProcessingTask.objects.get(id=task_id)
        except ImageProcessingTask.DoesNotExist:
            print(f"Task with ID: {task_id} does not exist")
            return False

        # change the status of the task to processing
        task.status = "processing"
        task.save()
        processing_started_at = time.time()

        # get the image
        original_image_url = task.original_image_url

        file_name = "original/" + original_image_url.split("/")[-1]
        original_img_np = self.blob_storage.get_img_data(file_name)

        assert (
            original_img_np is not None and type(original_img_np) == np.ndarray
        ), "Failed to get image data"
        # process the image
        processed_image_byte = process_image(original_img_np)
        # upload the image
        file_name, file_extension = file_name.split(".")
        file_name = file_name.replace("original/", "")
        file_name = f"processed/{file_name}_processed.{file_extension}"
        processed_img_url = self.blob_storage.upload_file(
            processed_image_byte, file_name
        )
        processing_end_at = time.time()
        
        # Convert timestamps to datetime objects
        processing_start_time = datetime.fromtimestamp(processing_started_at)
        processing_end_time = datetime.fromtimestamp(processing_end_at)

        # update the task status to completed
        task.status = "completed"
        task.processing_start_time = processing_start_time
        task.processing_end_time = processing_end_time
        task.processed_image_url = processed_img_url
        task.save()

        return True

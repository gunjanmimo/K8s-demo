from message_queue.azure_message_queue import AzureImageMessageQueue
from image_processing import process_image

azure_message_queue_client = AzureImageMessageQueue()


def check_image_processing_message_queue():
    print("Checking message queue...")
    messages = azure_message_queue_client.pull_message()

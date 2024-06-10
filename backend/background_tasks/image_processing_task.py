# ---------------------------------LOCAL IMPORTS---------------------------------#
from message_queue.azure_message_queue import AzureImageMessageQueue
from image_processing import process_image

# Initialize the Azure message queue client
azure_message_queue_client = AzureImageMessageQueue()


def check_image_processing_message_queue():
    """
    Repeatedly called to pull messages from the Azure message queue and process them.

    The workflow involves:
    1. Pulling messages from the Azure message queue.
    2. Processing the images as specified by the messages.
    """
    print("Checking message queue...")
    azure_message_queue_client.pull_message()

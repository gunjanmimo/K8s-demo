import logging
from typing import List
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings
from PIL import Image
import numpy as np
from io import BytesIO

logger = logging.getLogger(__name__)


class AzureBlobStorage:
    def __init__(self):
        try:

            self.blob_service_client = BlobServiceClient(
                account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net",
                credential=settings.AZURE_ACCOUNT_KEY,
            )
            self.container_client = self.blob_service_client.get_container_client(
                settings.AZURE_CONTAINER_NAME
            )
            logger.info("AzureBlobStorage initialized successfully.")
        except Exception as e:
            logger.error("Failed to initialize AzureBlobStorage: %s", e)
            raise

    def upload_file(self, file: bytes, file_name: str) -> str:
        try:
            blob_client = self.container_client.get_blob_client(file_name)
            blob_client.upload_blob(file, overwrite=True)
            logger.info("File '%s' uploaded successfully.", file_name)
            return blob_client.url
        except Exception as e:
            logger.error("Failed to upload file '%s': %s", file_name, e)
            raise

    # get the image data from the blob storage
    def get_img_data(self, file_name: str) -> np.ndarray:
        blob_client = self.container_client.get_blob_client(file_name)
        try:
            data = blob_client.download_blob()
            image_data = data.readall()

            # Convert the image data to a numpy array
            image = Image.open(BytesIO(image_data))
            img_array = np.array(image)

            return img_array
        except Exception as e:
            logger.error("Failed to get image data: %s", e)
            raise

    def download_file(self, file_name: str, local_path: str) -> bool:
        blob_client = self.container_client.get_blob_client(file_name)
        try:
            with open(local_path, "wb") as f:
                data = blob_client.download_blob()
                data.readinto(f)
            logger.info(
                "File '%s' downloaded successfully to '%s'.", file_name, local_path
            )
            return True
        except Exception as e:
            logger.error(
                "Failed to download file '%s' to '%s': %s", file_name, local_path, e
            )
            return False

    def delete_file(self, file_name: str) -> bool:
        blob_client = self.container_client.get_blob_client(file_name)
        try:
            blob_client.delete_blob()
            logger.info("File '%s' deleted successfully.", file_name)
            return True
        except Exception as e:
            logger.error("Failed to delete file '%s': %s", file_name, e)
            return False

    def get_all_files(self) -> List[str]:
        try:
            files = [blob.name for blob in self.container_client.list_blobs()]
            logger.info("Retrieved all files successfully.")
            return files
        except Exception as e:
            logger.error("Failed to list files: %s", e)
            raise

    def get_file_url(self, file_name: str) -> str:
        try:
            blob_client = self.container_client.get_blob_client(file_name)
            file_url = blob_client.url
            logger.info("URL for file '%s' retrieved successfully.", file_name)
            return file_url
        except Exception as e:
            logger.error("Failed to get URL for file '%s': %s", file_name, e)
            raise

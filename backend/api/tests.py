# --------------------------------PYTHON IMPORTS--------------------------------#
import tempfile
from PIL import Image
import io

# --------------------------------DJANGO IMPORTS--------------------------------#
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class APITestCase(TestCase):
    """
    Test case for the Image Processing API.

    This test case covers the following functionalities:
    1. Image upload
    2. Listing all image processing tasks
    3. Retrieving details of a specific task
    """

    def setUp(self):
        """
        Set up the test case with a Django test client.
        """
        self.client = Client()

    def create_temp_image(self):
        """
        Create a temporary image file for testing.

        Returns:
            A NamedTemporaryFile object containing a simple image.
        """
        # Create a temporary image
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file

    def test_image_upload(self):
        """
        Test the image upload functionality.

        This test uploads an image and checks if the response is correct.
        """
        url = reverse("upload")
        temp_image = self.create_temp_image()
        with open(temp_image.name, "rb") as image_file:
            response = self.client.post(url, {"image": image_file}, format="multipart")

        # Check if the response status is HTTP 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response contains the expected fields
        self.assertIn("id", response.json())
        self.assertIn("original_image_url", response.json())
        self.assertEqual(response.json()["status"], "pending")

        # Delete the temporary file
        temp_image.close()

    def test_list_tasks(self):
        """
        Test listing all image processing tasks.

        This test retrieves the list of tasks and verifies the response format.
        """
        url = reverse("tasks")
        response = self.client.get(url)

        # Check if the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response is a list
        self.assertIsInstance(response.json(), list)

        # If there are tasks, check if they contain the expected fields
        if response.json():
            self.assertIn("id", response.json()[0])
            self.assertIn("original_image_url", response.json()[0])
            self.assertIn("status", response.json()[0])

    def test_task_detail(self):
        """
        Test retrieving the details of a specific task.

        This test uploads an image to create a task and then retrieves its details.
        """
        # Create a task by uploading an image
        url = reverse("upload")
        temp_image = self.create_temp_image()
        with open(temp_image.name, "rb") as image_file:
            response = self.client.post(url, {"image": image_file}, format="multipart")

        # Check if the task was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_id = response.json()["id"]

        # Retrieve the details of the created task
        url = reverse("task-detail", args=[task_id])
        response = self.client.get(url)

        # Check if the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the expected fields
        self.assertIn("id", response.json())
        self.assertIn("original_image_url", response.json())
        self.assertIn("processed_image_url", response.json())
        self.assertIn("status", response.json())

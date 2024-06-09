from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import tempfile
from PIL import Image
import io



class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def create_temp_image(self):
        # Create a temporary image for testing
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file

    def test_image_upload(self):
        url = reverse('upload')
        temp_image = self.create_temp_image()
        with open(temp_image.name, 'rb') as image_file:
            response = self.client.post(url, {'image': image_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())
        self.assertIn('original_image_url', response.json())
        self.assertEqual(response.json()['status'], 'pending')
        
        # delete the temporary file
        temp_image.close()

    def test_list_tasks(self):
        url = reverse('tasks')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        if response.json():
            self.assertIn('id', response.json()[0])
            self.assertIn('original_image_url', response.json()[0])
            self.assertIn('status', response.json()[0])


    def test_task_detail(self):
        
        # Create a task
        url = reverse('upload')
        temp_image = self.create_temp_image()
        with open(temp_image.name, 'rb') as image_file:
            response = self.client.post(url, {'image': image_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_id = response.json()['id']
        url = reverse('task-detail', args=[task_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertIn('original_image_url', response.json())
        self.assertIn('processed_image_url', response.json())
        self.assertIn('status', response.json())
       
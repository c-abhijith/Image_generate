from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from images.models import GeneratedImage  # Import your model if needed

class GenerateImagesViewTestCase(APITestCase):

    @patch('images.tasks.generate_image.delay')
    def test_post_valid_prompts(self, mock_generate_image):
        mock_generate_image.return_value.id = 'mock-task-id'
        url = reverse('generate_images')
        response = self.client.post(url, {'prompts': ['Test prompt 1', 'Test prompt 2']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(response.data['data']), 2)
        self.assertIn('task_id', response.data['data'][0])

    def test_post_no_prompts(self):
        url = reverse('generate_images')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'At least one prompt is required.')

    @patch('images.tasks.generate_image.delay')
    def test_post_invalid_prompt_format(self, mock_generate_image):
        url = reverse('generate_images')
        response = self.client.post(url, {'prompts': 'Invalid format'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'At least one prompt is required.')

    def test_get_images(self):
        GeneratedImage.objects.create(task_id='test-task-id', image='http://example.com/image.jpg', prompt='Test prompt')
        url = reverse('generate_images')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['data']), 0)
        self.assertEqual(response.data['data'][0]['task_id'], 'test-task-id')
        self.assertEqual(response.data['data'][0]['image'], 'http://example.com/image.jpg')

    def test_get_no_images(self):
        url = reverse('generate_images')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data'], [])

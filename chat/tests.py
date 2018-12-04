from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .views import ChatTreeView,ChatbotView



class ChatTreeViewTest(TestCase):

    def test_file_is_accepted(self):

        file_path = "chat/test_data/demo.json"
        file_obj = open(file_path)
        file_obj.seek(0)
        url = reverse('chattree')


        data = {
            'file': file_obj,
            'name': 'Food choices'
        }

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_non_json_file_rejected(self):

        file_path = "chat/test_data/nonjson.js"
        file_obj = open(file_path)
        file_obj.seek(0)
        url = reverse('chattree')


        data = {
            'file': file_obj,
            'name': 'Food choices'
        }

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


    def test_broken_json_rejected(self):

        file_path = "chat/test_data/demo_brokenjson.json"
        file_obj = open(file_path)
        file_obj.seek(0)
        url = reverse('chattree')


        data = {
            'file': file_obj,
            'name': 'Food choices'
        }

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


    def test_db_value_insertion(self):
        file_path = "chat/test_data/demo.json"
        file_obj = open(file_path)
        file_obj.seek(0)
        url = reverse('chattree')

        data = {
            'file': file_obj,
            'name': 'Food'
        }

        self.client.post(url, data)

        url = reverse('questions-list')

        import json

        file_obj.seek(0)
        data = json.loads(file_obj.read())

        count = len(data)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.assertEqual(len(response.json()),count)


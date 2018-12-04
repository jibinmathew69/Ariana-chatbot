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




class ChatbotTest(TestCase):

    def setUp(self):
        file_path = "chat/test_data/demo.json"
        file_obj = open(file_path)
        file_obj.seek(0)
        url = reverse('chattree')

        data = {
            'file': file_obj,
            'name': 'Food choices'
        }

        self.client.post(url, data)


    def test_query_completion(self):
        queries = [
            "",
            "Yes",
            "Pizza",
            "Yes",
            ""
        ]

        url = reverse('chatbot')

        for query in queries:
            response = self.client.post(url, {
                'message': query,
                'questionaire' : 1
            })


        self.assertEqual(response.json(), "Restarting Conversation: Are you hungry?->Yes->Pizza->Yes")


    def test_query_completion2(self):
        queries = [
            "",
            "Yes",
            "Hamburger",
            ""
        ]

        url = reverse('chatbot')

        for query in queries:
            response = self.client.post(url, {
                'message': query,
                'questionaire': 1
            })


        self.assertEqual(response.json(), "Restarting Conversation: Are you hungry?->Yes->Hamburger")


    def test_query_completion_case_ignore(self):
        queries = [
            "",
            "no",
            ""
        ]

        url = reverse('chatbot')

        for query in queries:
            response = self.client.post(url, {
                'message': query,
                'questionaire': 1
            })


        self.assertEqual(response.json(), "Restarting Conversation: Are you hungry?->no")


    def test_query_invalid_option(self):
        queries = [
            "",
            "Yes",
            "piza"
        ]

        url = reverse('chatbot')

        for query in queries:
            response = self.client.post(url, {
                'message': query,
                'questionaire': 1
            })


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_query_invalid_questionaire(self):
        queries = [
            "",
        ]

        url = reverse('chatbot')

        for query in queries:
            response = self.client.post(url, {
                'message': query,
                'questionaire': 2
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_query_message_missing(self):


        url = reverse('chatbot')


        response = self.client.post(url, {
                'questionaire': 1
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        response = self.client.post(url, {
            'questionaire': 1
        })

        self.assertEqual(response.json(), "Invalid input")

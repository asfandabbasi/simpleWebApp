from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class InvoiceIngestionTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='foo', password='bar')
        token = Token.objects.create(user=cls.user)
        # Get user and assign license

        # Login
        cls.api_client = APIClient()
        # cls.api_client.login(username='foo', password='bar')
        cls.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        super().setUpClass()

    def test_upload_file_view(self):
        """Check the response of the api if it matches the expected code"""
        path = '/home/beedata/Documents/uni/DataIngestionWebApp/pythonProject/WebApp/sample_data/Tech task data - Sheet1.csv'
        files = {"upload_file": open(path, "r")}

        response = self.api_client.post(
            '/data-ingestion/invoices-upload/', files
        )
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

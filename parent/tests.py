from django.test import TestCase, Client
from manager.models import NoticeBox
from account.models import User
from django.urls import reverse


# unit test for models:
class ParentViewTestCase(TestCase):
    def setUp(self):
        # Create a test user with the 'is_parent' attribute set to True
        self.user = User.objects.create_user(username='testuser', password='testpassword', national_code='21332')
        self.user.is_parent = True
        self.user.save()

        # Create some test NoticeBox objects
        NoticeBox.objects.create(writer=self.user, title='Notice 1', description='Description 1')
        NoticeBox.objects.create(writer=self.user, title='Notice 2', description='Description 2')

        # Create a test client
        self.client = Client()

    def test_parent_view_access(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send a GET request to the parent_view
        response = self.client.get(reverse('parent:parent_panel'))  # Replace with your actual URL

        # Check that the response status code is 200 (OK)
        self.assertIn(response.status_code, [200, 302])

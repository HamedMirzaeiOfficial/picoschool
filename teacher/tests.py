from django.test import TestCase
from django.urls import reverse
from account.models import User

# unit test for urls:
class TestTeacherViews(TestCase):
    def setUp(self):
        # Create a user with teacher role for testing (adjust fields as needed)
        self.user = User.objects.create_user(
            username='testteacher',
            password='testpassword',
            # Add other required fields here
        )
        # Set the user's role to teacher (adjust this based on your implementation)
        self.user.is_teacher = True
        self.user.save()

    def test_teacher_view(self):
        # Log in the user
        self.client.login(username='testteacher', password='testpassword')

        url = reverse('teacher:teacher_panel')
        response = self.client.get(url)

        self.assertIn(response.status_code, [200, 302])


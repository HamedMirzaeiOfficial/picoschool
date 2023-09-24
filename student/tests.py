from django.test import TestCase
from django.urls import reverse
from account.models import User


# unit test for urls:
class TestStudentUrls(TestCase):
    def test_student_panel_url(self):
        url = reverse('student:student_panel')
        self.assertEqual(url, '/student/')

    def test_create_emp_form_url(self):
        url = reverse('student:create_emp_form')
        self.assertEqual(url, '/student/create-emp-form/')



# unit test for views:
from django.test import TestCase
from django.urls import reverse

class TestStudentViews(TestCase):
    def setUp(self):
        # Create a user for testing (adjust fields as needed)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            # Add other required fields here
        )

    def test_student_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        url = reverse('student:student_panel')
        response = self.client.get(url)

        self.assertIn(response.status_code, [200, 302])
   
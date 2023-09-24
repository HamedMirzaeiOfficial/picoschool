from django.test import TestCase, Client
from main.models import SiteSetting
from django.urls import reverse
from account.models import User


# unit test for models:
class SiteSettingModelTestCase(TestCase):

    def test_create_site_setting_instance(self):
        # Create a SiteSetting instance and save it to the database
        school_name = 'Sample School'
        site_setting = SiteSetting.objects.create(
            school_name=school_name,
            site_color='green',
            site_menu_theme='waterfall'
        )

        # Retrieve the SiteSetting instance from the database
        retrieved_site_setting = SiteSetting.objects.get(school_name=school_name)

        # Assert that the retrieved instance matches the created one
        self.assertEqual(site_setting, retrieved_site_setting)

    def test_str_representation(self):
        # Create a SiteSetting instance
        school_name = 'Sample School'
        site_setting = SiteSetting.objects.create(
            school_name=school_name,
            site_color='green',
            site_menu_theme='waterfall'
        )

        # Check the string representation of the instance
        self.assertEqual(str(site_setting), school_name)

    def test_default_values(self):
        # Create a SiteSetting instance without specifying optional fields
        school_name = 'Sample School'
        site_setting = SiteSetting.objects.create(school_name=school_name)

        # Retrieve the instance and check the default values
        retrieved_site_setting = SiteSetting.objects.get(school_name=school_name)
        self.assertEqual(retrieved_site_setting.site_color, 'green')
        self.assertEqual(retrieved_site_setting.site_menu_theme, 'waterfall')

#  unit test for views:
class MainViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view_anonymous_user(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to another view

    def test_events_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('main:events'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

    def test_events_view_anonymous_user(self):
        response = self.client.get(reverse('main:events'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to login


# unit test for urls:
class TestUrls(TestCase):
    def test_index_url(self):
        # Test the URL pattern for the index view
        url = reverse('main:index')
        self.assertEqual(url, '/')  # Ensure the URL is correct

    def test_events_url(self):
        # Test the URL pattern for the events view
        url = reverse('main:events')
        self.assertEqual(url, '/pages/events/')

    def test_notice_box_url(self):
        # Test the URL pattern for the notice_box view
        url = reverse('main:notices')
        self.assertEqual(url, '/pages/notices/')

    def test_student_detail_url(self):
        # Test the URL pattern for the student_detail view with a specific student ID
        student_id = 1  # Replace with a valid student ID
        url = reverse('main:student_detail', args=[student_id])
        self.assertEqual(url, f'/student/{student_id}/detail/')



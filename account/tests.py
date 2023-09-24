from django.test import TestCase, Client
from .models import User, Grade, Major
from django.contrib.auth import get_user_model
from django.urls import reverse
from account.models import User


# unit test for models:
class UserModelTestCase(TestCase):
    def setUp(self):
        # Create test instances for related models (Grade and Major)
        self.grade = Grade.objects.create(name='Test Grade')
        self.major = Major.objects.create(name='Test Major')

        # Create a sample User instance for testing
        self.user = User.objects.create(
            username='test_user',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            is_manager=True,
            is_student=True,
            national_code='1234567890',
            address='123 Test Street',
            student_class=None,  # You can set this to a specific class if needed
            grade=self.grade,
            major=self.major,
            date_of_birth='2000-01-01',
            is_active=True,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'test_user')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertTrue(self.user.is_manager)
        self.assertTrue(self.user.is_student)
        self.assertEqual(self.user.national_code, '1234567890')
        self.assertEqual(self.user.address, '123 Test Street')
        self.assertIsNone(self.user.student_class)
        self.assertEqual(self.user.grade, self.grade)
        self.assertEqual(self.user.major, self.major)
        self.assertEqual(self.user.date_of_birth, '2000-01-01')
        self.assertTrue(self.user.is_active)

    def test_parent_count_property(self):
        # Create a test parent user
        User.objects.create(username='parent_user', is_parent=True, is_active=True)
        self.assertEqual(self.user.parent_count, 1)

    def test_teacher_count_property(self):
        # Create a test teacher user
        User.objects.create(username='teacher_user', is_teacher=True, is_active=True)
        self.assertEqual(self.user.teacher_count, 1)

    def test_student_count_property(self):
        # Create a test student user
        User.objects.create(username='student_user', is_student=True, is_active=True)
        self.assertEqual(self.user.student_count, 2)


# integration test for models:
class UserModelIntegrationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create some test data that can be used in multiple test methods
        cls.grade = Grade.objects.create(name='Test Grade')
        cls.major = Major.objects.create(name='Test Major')

    def create_test_users(self):
        # Create test users for different roles
        student = get_user_model().objects.create(
            username='student_username',
            national_code='12344', 
            is_student=True,
            grade=self.grade,
            major=self.major,
            date_of_birth='2000-01-01',
        )
        teacher = get_user_model().objects.create(
            username='teacher_username',
            national_code='123244', 
            is_teacher=True,
            university='Test University',
        )
        parent = get_user_model().objects.create(
            username='parent_username',
            national_code='1231344', 
            is_parent=True,
        )

        # Ensure the users are active
        student.is_active = True
        teacher.is_active = True
        parent.is_active = True

        student.save()
        teacher.save()
        parent.save()

    def test_parent_count(self):
        self.create_test_users()
        
        # Retrieve the user count with the 'is_parent' flag and active status
        parent_count = get_user_model().objects.filter(is_parent=True, is_active=True).count()
        
        # Test that the count matches the expected count (1 in this case)
        self.assertEqual(parent_count, 1)

    def test_teacher_count(self):
        self.create_test_users()
        
        # Retrieve the user count with the 'is_teacher' flag and active status
        teacher_count = get_user_model().objects.filter(is_teacher=True, is_active=True).count()
        
        # Test that the count matches the expected count (1 in this case)
        self.assertEqual(teacher_count, 1)

    def test_student_count(self):
        self.create_test_users()
        
        # Retrieve the user count with the 'is_student' flag and active status
        student_count = get_user_model().objects.filter(is_student=True, is_active=True).count()
        
        # Test that the count matches the expected count (1 in this case)
        self.assertEqual(student_count, 1)

    # Add more test methods for other user-related functionality as needed


# regression test for models:
class UserModelRegressionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create some initial test data that your regression tests can rely on
        cls.grade = Grade.objects.create(name='Test Grade')
        cls.major = Major.objects.create(name='Test Major')

    def test_create_student(self):
        user = get_user_model().objects.create(
            username='student_username',
            national_code = '124233',
            is_student=True,
            grade=self.grade,
            major=self.major,
            date_of_birth='2000-01-01',
        )

        # Check that the user was created successfully
        self.assertEqual(get_user_model().objects.count(), 1)

        # Check that the user's fields match the expected values
        self.assertEqual(user.is_student, True)
        self.assertEqual(user.grade, self.grade)
        self.assertEqual(user.major, self.major)
        self.assertEqual(user.date_of_birth, '2000-01-01')

    def test_create_teacher(self):
        user = get_user_model().objects.create(
            username='teacher_username',
            is_teacher=True,
            university='Test University',
        )

        # Check that the user was created successfully
        self.assertEqual(get_user_model().objects.count(), 1)

        # Check that the user's fields match the expected values
        self.assertEqual(user.is_teacher, True)
        self.assertEqual(user.university, 'Test University')

    def test_create_parent(self):
        user = get_user_model().objects.create(
            username='parent_username',
            is_parent=True,
        )

        # Check that the user was created successfully
        self.assertEqual(get_user_model().objects.count(), 1)

        # Check that the user's fields match the expected values
        self.assertEqual(user.is_parent, True)

    # Add more regression test methods for other user-related functionality as needed


# unit test for views:
class ViewsUnitTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'national_code': '1234567890',
        }
        cls.user = User.objects.create_user(**cls.user_data)

    def test_login_view_get(self):
        # Test the GET request to the login view
        client = Client()
        response = client.get(reverse('account:login'))

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_successful_login(self):
        # Test a successful POST request to the login view
        client = Client()
        response = client.post(reverse('account:login'), self.user_data, follow=True)

        # Assert that the user is logged in
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        # Test a POST request to the login view with invalid credentials
        client = Client()
        response = client.post(reverse('account:login'), {'username': 'invaliduser', 'password': 'invalidpassword'})

        # Assert that the response does not contain a redirect
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains an error message
        self.assertContains(response, 'نام کاربری یا گذرواژه وارد شده نادرست است')

    def test_change_password_view_get(self):
        # Test the GET request to the change password view
        client = Client()
        client.login(username=self.user.username, password='testpassword')
        response = client.get(reverse('account:change_password'))

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)


# end to end test for views:
class ViewsEndToEndTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'national_code': '1234567890',
            # Add other required fields for user creation
        }
        cls.user = User.objects.create_user(**cls.user_data)

    def test_login_view_successful_login(self):
        # Simulate a successful login process
        client = Client()
        response = client.post(reverse('account:login'), self.user_data, follow=True)

     
        # Assert that the user is logged in
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_invalid_credentials(self):
        # Simulate a login attempt with invalid credentials
        client = Client()
        response = client.post(reverse('account:login'), {'username': 'invaliduser', 'password': 'invalidpassword'})

        # Assert that the response contains an error message
        self.assertContains(response, 'نام کاربری یا گذرواژه وارد شده نادرست است')


# unit test for urls:
class UrlsUnitTestCase(TestCase):

    def test_login_url_resolves_to_login_view(self):
        # Test that the login URL resolves to the login_view function
        url = reverse('account:login')
        self.assertEqual(url, '/login/')  # Ensure the URL pattern is as expected
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Ensure the view is callable

    def test_logout_url_resolves_to_logout_view(self):
        # Test that the logout URL resolves to the LogoutView class
        url = reverse('account:logout')
        self.assertEqual(url, '/logout/')  # Ensure the URL pattern is as expected

    def test_change_password_url_resolves_to_change_password_view(self):
        # Test that the change_password URL resolves to the ChangePasswordView class
        url = reverse('account:change_password')
        self.assertEqual(url, '/user/password-change/')  # Ensure the URL pattern is as expected


# none functional test for urls:
class UrlsNonFunctionalTestCase(TestCase):

    def test_url_structure(self):
        # Test the structure of your URLs to ensure they follow a consistent pattern
        login_url = reverse('account:login')
        self.assertEqual(login_url, '/login/')  # Ensure the URL structure is as expected

        logout_url = reverse('account:logout')
        self.assertEqual(logout_url, '/logout/')

        change_password_url = reverse('account:change_password')
        self.assertEqual(change_password_url, '/user/password-change/')

        user_password_done_url = reverse('account:user_password_done')
        self.assertEqual(user_password_done_url, '/user/password-done/')

    def test_url_naming_conventions(self):
        # Test that your URL names follow consistent naming conventions
        login_url = reverse('account:login')
        self.assertEqual(login_url, '/login/')  # Ensure the URL name is appropriate

        logout_url = reverse('account:logout')
        self.assertEqual(logout_url, '/logout/')

        change_password_url = reverse('account:change_password')
        self.assertEqual(change_password_url, '/user/password-change/')

        user_password_done_url = reverse('account:user_password_done')
        self.assertEqual(user_password_done_url, '/user/password-done/')

    def test_url_security(self):
        # Test the security of your URLs, ensuring that they are not susceptible to common security issues
        login_url = reverse('account:login')
        self.assertTrue(login_url.startswith('/login/'))  # Ensure the URL is secure (e.g., no sensitive data in the URL)

        logout_url = reverse('account:logout')
        self.assertTrue(logout_url.startswith('/logout/'))

        change_password_url = reverse('account:change_password')
        self.assertTrue(change_password_url.startswith('/user/password-change/'))

        user_password_done_url = reverse('account:user_password_done')
        self.assertTrue(user_password_done_url.startswith('/user/password-done/'))

    def test_url_performance(self):
        # Measure the performance of your URLs by sending multiple requests and checking response times
        import time

        start_time = time.time()
        for _ in range(10):
            self.client.get(reverse('account:login'))
        end_time = time.time()

        elapsed_time = end_time - start_time
        self.assertTrue(elapsed_time < 1.0)  # Ensure URL response times are within acceptable limits




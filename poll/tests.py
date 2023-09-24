from django.test import TestCase, Client
from django.utils import timezone
from account.models import User
from .models import Poll, PollOptions
from django.urls import reverse
from .forms import CreatePollForm
from django.http import JsonResponse


# unit test for models:
class PollModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_poll_creation(self):
        # Create a new poll
        poll = Poll.objects.create(
            question='Test Question',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Add the test user to the poll's users
        poll.users.add(self.user)

        # Check if the poll was created successfully
        self.assertEqual(poll.question, 'Test Question')
        self.assertTrue(poll.active)
        self.assertEqual(poll.for_user, 'all')
        self.assertEqual(poll.users.count(), 1)

    def test_poll_options_creation(self):
        # Create a new poll
        poll = Poll.objects.create(
            question='Test Question',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Create poll options
        option1 = PollOptions.objects.create(poll=poll, option='Option 1')
        option2 = PollOptions.objects.create(poll=poll, option='Option 2')

        # Check if the poll options were created successfully
        self.assertEqual(option1.option, 'Option 1')
        self.assertEqual(option2.option, 'Option 2')
        self.assertEqual(option1.poll, poll)
        self.assertEqual(option2.poll, poll)

    def test_poll_options_count(self):
        # Create a new poll
        poll = Poll.objects.create(
            question='Test Question',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Create poll options
        option1 = PollOptions.objects.create(poll=poll, option='Option 1')
        option2 = PollOptions.objects.create(poll=poll, option='Option 2')

        # Increase the count of option 1
        option1.option_count += 1
        option1.save()

        # Check if the count of option 1 is updated correctly
        self.assertEqual(option1.option_count, 1)

    def test_poll_all_count_property(self):
        # Create multiple polls
        poll1 = Poll.objects.create(
            question='Poll 1',
            active=True,
            for_user='all',
            create=timezone.now(),
        )
        poll2 = Poll.objects.create(
            question='Poll 2',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Check if the 'all_count' property returns the correct count of polls
        self.assertEqual(poll1.all_count, 2)
        self.assertEqual(poll2.all_count, 2)

    def test_poll_options_str_method(self):
        # Create a new poll
        poll = Poll.objects.create(
            question='Test Question',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Create a poll option
        option = PollOptions.objects.create(poll=poll, option='Test Option')

        # Check if the 'str' method of PollOptions returns the option text
        self.assertEqual(str(option), 'Test Option')


# integration test for models:
class ModelsIntegrationTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_poll_with_options_creation(self):
        # Create a new poll
        poll = Poll.objects.create(
            question='Test Question',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Add the test user to the poll's users
        poll.users.add(self.user)

        # Create poll options
        option1 = PollOptions.objects.create(poll=poll, option='Option 1')
        option2 = PollOptions.objects.create(poll=poll, option='Option 2')

        # Check if the poll and options were created successfully
        self.assertEqual(poll.question, 'Test Question')
        self.assertTrue(poll.active)
        self.assertEqual(poll.for_user, 'all')
        self.assertEqual(poll.users.count(), 1)
        self.assertEqual(option1.option, 'Option 1')
        self.assertEqual(option2.option, 'Option 2')
        self.assertEqual(option1.poll, poll)
        self.assertEqual(option2.poll, poll)

    def test_poll_with_options_count(self):
        # Create a new poll
        poll = Poll.objects.create(
            question='Test Question',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Add the test user to the poll's users
        poll.users.add(self.user)

        # Create poll options
        option1 = PollOptions.objects.create(poll=poll, option='Option 1')
        option2 = PollOptions.objects.create(poll=poll, option='Option 2')

        # Increase the count of option 1
        option1.option_count += 1
        option1.save()

        # Check if the count of option 1 is updated correctly
        self.assertEqual(option1.option_count, 1)


# integration test for models:
class PollIntegrationTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a poll
        self.poll = Poll.objects.create(
            question='Test Question',
            active=True,
            for_user='all',
            create=timezone.now(),
        )

        # Create poll options
        self.option1 = PollOptions.objects.create(
            poll=self.poll,
            option='Option 1',
            option_count=0,
        )
        self.option2 = PollOptions.objects.create(
            poll=self.poll,
            option='Option 2',
            option_count=0,
        )

    def test_poll_options_relationship(self):
        # Test whether the poll options are correctly related to the poll
        self.assertEqual(list(self.poll.poll_option.all()), [self.option1, self.option2])
        self.assertEqual(self.option1.poll, self.poll)
        self.assertEqual(self.option2.poll, self.poll)

    def test_user_relationship(self):
        # Test whether users are correctly related to the poll
        self.poll.users.add(self.user)

        self.assertEqual(list(self.poll.users.all()), [self.user])
        self.assertEqual(list(self.user.poll_user.all()), [self.poll])

    def test_poll_options_voting_relationship(self):
        # Test whether voting for options updates the count correctly and maintains relationships
        self.option1.option_count += 1
        self.option2.option_count += 1
        self.option1.save()
        self.option2.save()
        self.option1.refresh_from_db()
        self.option2.refresh_from_db()

        self.assertEqual(self.option1.option_count, 1)
        self.assertEqual(self.option2.option_count, 1)

        self.assertEqual(list(self.poll.poll_option.all()), [self.option1, self.option2])


# unit test for urls:
class PollURLsTestCase(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(question='Test Poll', active=True, for_user='all')

    def test_poll_list_url(self):
        response = self.client.get(reverse('poll:poll_list'))
        self.assertIn(response.status_code, [200, 302])

    def test_poll_options_list_url(self):
        response = self.client.get(reverse('poll:poll_options_list', args=[self.poll.id]))
        self.assertIn(response.status_code, [200, 302])

    def test_poll_create_url(self):
        response = self.client.get(reverse('poll:poll_create'))
        self.assertIn(response.status_code, [200, 302])

    def test_poll_update_url(self):
        response = self.client.get(reverse('poll:poll_update', args=[self.poll.id]))
        self.assertIn(response.status_code, [200, 302])

    def test_poll_vote_url(self):
        response = self.client.get(reverse('poll:poll_vote', args=[self.poll.id]))
        self.assertIn(response.status_code, [200, 302])

    def test_poll_result_url(self):
        response = self.client.get(reverse('poll:poll_result', args=[self.poll.id]))
        self.assertIn(response.status_code, [200, 302])

    # Add more test cases as needed


# unit test for forms:
class CreatePollFormTestCase(TestCase):
    def test_create_poll_form_valid(self):
        form_data = {
            'question': 'Test Poll',
            'active': True,
            'for_user': 'all',
        }
        form = CreatePollForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_poll_form_blank_data(self):
        form = CreatePollForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # All fields are required

    def test_create_poll_form_placeholder(self):
        form = CreatePollForm()
        self.assertIn('placeholder="عنوان نظرسنجی را وارد کنید"', str(form))

    def test_create_poll_form_submission(self):
        form_data = {
            'question': 'Test Poll',
            'active': True,
            'for_user': 'all',
        }
        response = self.client.post(reverse('poll:poll_create'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Successful form submission


# unit test for views:
class PollViewsTestCase(TestCase):
    def setUp(self):
        # Create a user for testing (you can create other users as needed)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_poll_list_view_superuser(self):
        # Simulate a superuser login
        self.client.login(username='testuser', password='testpassword')

        # Create a sample poll
        poll = Poll.objects.create(question='Test Poll', active=True, for_user='all')

        response = self.client.get(reverse('poll:poll_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll/poll_list.html')

    # Add similar tests for other user types (e.g., student, parent, teacher)

    def test_poll_options_list_view(self):
        poll = Poll.objects.create(question='Test Poll', active=True, for_user='all')

        response = self.client.get(reverse('poll:poll_options_list', args=[poll.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll/poll_list.html')

    def test_poll_create_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('poll:poll_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll/poll_create.html')

    def test_poll_create_form_submission(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'question': 'Test Poll',
            'active': True,
            'for_user': 'all',
        }
        response = self.client.post(reverse('poll:poll_create'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Successful form submission
        self.assertEqual(Poll.objects.count(), 1)  # One Poll object should be created

    # Add tests for other views (PollUpdate, poll_vote, poll_result) as needed

    def test_poll_vote_view(self):
        poll = Poll.objects.create(question='Test Poll', active=True, for_user='all')
        option = PollOptions.objects.create(poll=poll, option='Option 1')

        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('poll:poll_vote', args=[poll.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll/poll_vote.html')

        # Simulate a POST request for voting
        response = self.client.post(reverse('poll:poll_vote', args=[poll.pk]), data={'option': option.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)  # Ensure a JSON response is returned


# integration test for views:
class PollIntegrationTestCase(TestCase):
    def setUp(self):
        # Create a user for testing (you can create other users as needed)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_poll_creation_and_voting(self):
        # Simulate a user login
        self.client.login(username='testuser', password='testpassword')

        # Create a poll
        response = self.client.post(reverse('poll:poll_create'), data={
            'question': 'Test Poll',
            'active': True,
            'for_user': 'all',
        })

        self.assertEqual(response.status_code, 302)  # Successful form submission
        self.assertEqual(Poll.objects.count(), 1)  # One Poll object should be created

        poll = Poll.objects.first()

        # Create poll options
        response = self.client.post(reverse('poll:poll_options_list', args=[poll.pk]), data={
            'poll': poll.pk,
            'option': 'Option 1',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)  # Successful AJAX request
        self.assertEqual(PollOptions.objects.count(), 1)  # One PollOptions object should be created

        option = PollOptions.objects.first()

        # Vote in the poll
        response = self.client.post(reverse('poll:poll_vote', args=[poll.pk]), data={'option': option.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        # Check if the vote count increased
        option.refresh_from_db()
        self.assertEqual(option.option_count, 1)

    # Add more integration tests for other view interactions as needed


# regression test for views:
class PollRegressionTestCase(TestCase):
    def setUp(self):
        # Create a user for testing (you can create other users as needed)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_poll_creation_and_voting_regression(self):
        # Simulate a user login
        self.client.login(username='testuser', password='testpassword')

        # Create a poll
        response = self.client.post(reverse('poll:poll_create'), data={
            'question': 'Test Poll',
            'active': True,
            'for_user': 'all',
        })

        self.assertEqual(response.status_code, 302)  # Successful form submission
        self.assertEqual(Poll.objects.count(), 1)  # One Poll object should be created

        poll = Poll.objects.first()

        # Create poll options
        response = self.client.post(reverse('poll:poll_options_list', args=[poll.pk]),
                                     data={
            'poll': poll.pk,
            'option': 'Option 1',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)  # Successful AJAX request
        self.assertEqual(PollOptions.objects.count(), 1)  # One PollOptions object should be created

        option = PollOptions.objects.first()

        # Vote in the poll
        response = self.client.post(reverse('poll:poll_vote', args=[poll.pk]), data={'option': option.pk},
                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        # Check if the vote count increased
        option.refresh_from_db()
        self.assertEqual(option.option_count, 1)

        # Regression test: Check if the poll result view works correctly
        response = self.client.get(reverse('poll:poll_result', args=[poll.pk]))
        self.assertEqual(response.status_code, 200)



# system end to end test for views:
class PollSystemEndToEndTestCase(TestCase):
    def setUp(self):
        # Create a user for testing (you can create other users as needed)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_system_end_to_end(self):
        # Initialize the Django test client
        client = Client()

        # Simulate a user login
        client.login(username='testuser', password='testpassword')

        # Create a poll using a POST request
        create_poll_url = reverse('poll:poll_create')
        create_poll_data = {
            'question': 'Test Poll',
            'active': True,
            'for_user': 'all',
        }
        response = client.post(create_poll_url, create_poll_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check if the poll was created successfully

       
        # Create poll options using a POST request
        create_options_url = reverse('poll:poll_options_list', args=[1])  # Assuming poll ID is 1
        create_options_data = {
            'poll': 1,
            'option': 'Option 1',
        }
        response = client.post(create_options_url, create_options_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)  # Check if the options were created successfully

        # Vote in the poll using a POST request
        vote_url = reverse('poll:poll_vote', args=[1])  # Assuming poll ID is 1
        vote_data = {'option': 1}  # Assuming option ID is 1
        response = client.post(vote_url, vote_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)  # Check if the vote was successful

        # Check if the poll result page is displayed
        poll_result_url = reverse('poll:poll_result', args=[1])  # Assuming poll ID is 1
        response = client.get(poll_result_url)
        self.assertEqual(response.status_code, 200)  # Check if the result page is accessible

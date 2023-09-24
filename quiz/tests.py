from django.test import TestCase
from django.utils import timezone
from account.models import User
from manager.models import Classes, Books
from .models import Quiz, QuizQuestion, QuizMultipleAnswers, QuizDescAnswers, QuizResult
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quiz import views

# unit tests for models:
class QuizModelTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.quiz_class = Classes.objects.create(name='Test Class')
        self.quiz_book = Books.objects.create(name='Test Book', units=3)
        self.quiz = Quiz.objects.create(
            name='Test Quiz',
            topic='Test Topic',
            quiz_class=self.quiz_class,
            quiz_book=self.quiz_book,
            number_of_question=10,
            time=30,
            show_quiz=True,
            required_score_to_pass=70,
            difficulty='ساده',
            active=True,
        )
        self.quiz.students.add(self.user)
        self.quiz_result = QuizResult.objects.create(
            quiz=self.quiz,
            user=self.user,
            data={'score': 80},
        )
        self.quiz_question = QuizQuestion.objects.create(
            id=1,
            text='Test Question',
            quiz=self.quiz,
            question_type='چهار گزینه ای',
        )
        self.quiz_multi_answer = QuizMultipleAnswers.objects.create(
            text='Test Answer',
            correct=True,
            question=self.quiz_question,
        )
        self.quiz_desc_answer = QuizDescAnswers.objects.create(
            text='Test Description Answer',
            question=self.quiz_question,
        )

    def test_quiz_model(self):
        quiz = Quiz.objects.get(name='Test Quiz')
        self.assertEqual(str(quiz), 'Test Quiz - ۱ مهر ۱۴۰۲ ')
        self.assertEqual(quiz.questions().count(), 1)

    def test_quiz_question_model(self):
        question = QuizQuestion.objects.get(text='Test Question')
        self.assertEqual(str(question), 'Test Question')

    def test_quiz_multi_answers_model(self):
        answer = QuizMultipleAnswers.objects.get(text='Test Answer')
        self.assertEqual(str(answer), 'Test Answer')

    def test_quiz_desc_answers_model(self):
        answer = QuizDescAnswers.objects.get(text='Test Description Answer')
        self.assertEqual(str(answer), 'Test Question')

    def test_quiz_result_model(self):
        result = QuizResult.objects.get(data__score=80)
        self.assertEqual(str(result), 'str(self.pk)')



# unit tests for urls:
class TestQuizUrls(SimpleTestCase):
    def test_quiz_list_url(self):
        url = reverse('quiz:quiz_list')
        self.assertEqual(resolve(url).func, views.quiz_list)

    def test_quiz_detail_url(self):
        url = reverse('quiz:quiz_detail', args=[1])
        self.assertEqual(resolve(url).func, views.quiz_detail)

    def test_quiz_start_url(self):
        url = reverse('quiz:quiz_start', args=[1, 'uuid'])
        self.assertEqual(resolve(url).func, views.quiz_start)

    def test_quiz_create_url(self):
        url = reverse('quiz:quiz_create')
        self.assertEqual(resolve(url).func.view_class, views.CreateQuiz)

    def test_quiz_update_url(self):
        url = reverse('quiz:quiz_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.UpdateQuiz)

    def test_quiz_questions_list_url(self):
        url = reverse('quiz:quiz_questions_list', args=[1])
        self.assertEqual(resolve(url).func, views.quiz_questions_list)

    def test_question_update_url(self):
        url = reverse('quiz:question_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.UpdateQuestion)

    def test_update_question_url(self):
        url = reverse('quiz:update_question')
        self.assertEqual(resolve(url).func, views.update_question)

    def test_update_answers_url(self):
        url = reverse('quiz:update_answers')
        self.assertEqual(resolve(url).func, views.update_answers)

    def test_create_answers_url(self):
        url = reverse('quiz:create_answers')
        self.assertEqual(resolve(url).func, views.create_answers)

    def test_get_questions_url(self):
        url = reverse('quiz:get_questions')
        self.assertEqual(resolve(url).func, views.get_questions)

    def test_answers_data_url(self):
        url = reverse('quiz:answers_data')
        self.assertEqual(resolve(url).func, views.answers_data)

    def test_result_list_url(self):
        url = reverse('quiz:result_list')
        self.assertEqual(resolve(url).func, views.result_list)

    def test_result_detail_url(self):
        url = reverse('quiz:result_detail', args=[1, 1])
        self.assertEqual(resolve(url).func, views.result_detail)

    def test_create_result_url(self):
        url = reverse('quiz:create_result')
        self.assertEqual(resolve(url).func, views.create_result)

    def test_create_result_2_url(self):
        url = reverse('quiz:create_result_2')
        self.assertEqual(resolve(url).func, views.create_result_2)

    def test_result_data_url(self):
        url = reverse('quiz:result_data', args=[1])
        self.assertEqual(resolve(url).func, views.result_data)



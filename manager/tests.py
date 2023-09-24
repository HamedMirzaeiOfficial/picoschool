from django.test import TestCase
from django.utils import timezone
from .models import (
    EventCalendar,
    ExternalEventCalendar,
    NoticeBox,
    Grade,
    Major,
    Classes,
    Books,
    Attendance,
    Assign,
    ReportCard,
    HomeWork,
    EmploymentForm,
)
from account.models import User
from django.urls import reverse
from quiz.models import Quiz
from .filters import StudentFilter, ParentFilter, TeacherFilter, ClassFilter, EMPFormFilter, QuizListFilter


# unit test for models:
class ModelTests(TestCase):
    def setUp(self):
        # Create some initial data for testing
        self.grade = Grade.objects.create(name='Grade 1')
        self.major = Major.objects.create(name='Math')
        self.classes = Classes.objects.create(
            name='Class A',
            code='101',
            grade=self.grade,
            major=self.major,
        )
        self.book = Books.objects.create(
            name='Math Book',
            units=3,
            grade=self.grade,
        )
        self.attendance = Attendance.objects.create(
            attendance_class=self.classes,
            book=self.book,
            date='1400-01-01',
        )
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.assign = Assign.objects.create(
            attendance=self.attendance,
            student=self.user,
            attendance_status='حاضر',
        )

    def test_event_calendar_model(self):
        event = EventCalendar.objects.create(
            title='Event 1',
            start='1400-01-01',
            end='1400-01-02',
            backgroundColor='red',
            borderColor='black',
        )
        self.assertEqual(event.jstart(), '1 0  778 ')  # Test jalali date conversion

    # Add similar tests for other models...

    def test_home_work_model(self):
        homework = HomeWork.objects.create(
            attendance=self.attendance,
            title='Homework 1',
            description='Complete exercises 1-5',
        )
        self.assertEqual(homework.date, '01 فروردین 1400')  # Test date property

    def test_employment_form_model(self):
        form = EmploymentForm.objects.create(
            student=self.user,
            organ='Company ABC',
            status='در انتظار بررسی',
        )
        self.assertEqual(form.all_count, 1)  # Test all_count property
    
    def test_assign_model(self):
        self.assertEqual(str(self.assign), 'Class A - 01 فروردین 1400 -  - حاضر')  # Test __str__ method

   
# integration test for models:
class ModelIntegrationTests(TestCase):
    def setUp(self):
        # Create some initial data for testing
        self.grade = Grade.objects.create(name='Grade 1')
        self.major = Major.objects.create(name='Math')
        self.classes = Classes.objects.create(
            name='Class A',
            code='101',
            grade=self.grade,
            major=self.major,
        )
        self.book = Books.objects.create(
            name='Math Book',
            units=3,
            grade=self.grade,
        )
        self.attendance = Attendance.objects.create(
            attendance_class=self.classes,
            book=self.book,
            date='1400-01-01',
        )
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.assign = Assign.objects.create(
            attendance=self.attendance,
            student=self.user,
            attendance_status='حاضر',
        )
        self.report_card = ReportCard.objects.create(
            student=self.user,
            report_card='This is a sample report card.',
        )
        self.homework = HomeWork.objects.create(
            attendance=self.attendance,
            title='Homework 1',
            description='Complete exercises 1-5',
        )
        self.form = EmploymentForm.objects.create(
            student=self.user,
            organ='Company ABC',
            status='در انتظار بررسی',
        )

  
    def test_attendance_with_assignments(self):
        # Ensure that assignments are associated with the correct attendance record
        assignment = Assign.objects.create(
            attendance=self.attendance,
            student=self.user,
            attendance_status='غایب',
        )
        self.assertEqual(assignment.attendance, self.attendance)

    def test_user_with_reports(self):
        # Ensure that user reports can be retrieved
        reports = ReportCard.objects.filter(student=self.user)
        self.assertEqual(reports.count(), 1)

    def test_attendance_with_homework(self):
        # Ensure that homework assignments are associated with the correct attendance record
        homework = HomeWork.objects.create(
            attendance=self.attendance,
            title='Homework 2',
            description='Complete exercises 6-10',
        )
        self.assertEqual(homework.attendance, self.attendance)

    def test_user_with_employment_forms(self):
        # Ensure that employment forms can be retrieved for a user
        forms = EmploymentForm.objects.filter(student=self.user)
        self.assertEqual(forms.count(), 1)

    def test_user_with_assignments(self):
        # Ensure that assignments can be retrieved for a user
        assignments = Assign.objects.filter(student=self.user)
        self.assertEqual(assignments.count(), 1)


# system/end to end test for models:
class ModelSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.grade = Grade.objects.create(name='Grade 1')
        self.major = Major.objects.create(name='Math')
        self.classes = Classes.objects.create(
            name='Class A',
            code='101',
            grade=self.grade,
            major=self.major,
        )
        self.book = Books.objects.create(
            name='Math Book',
            units=3,
            grade=self.grade,
        )
        self.attendance = Attendance.objects.create(
            attendance_class=self.classes,
            book=self.book,
            date='1400-01-01',
        )
        self.assign = Assign.objects.create(
            attendance=self.attendance,
            student=self.user,
            attendance_status='حاضر',
        )
        self.report_card = ReportCard.objects.create(
            student=self.user,
            report_card='This is a sample report card.',
        )
        self.homework = HomeWork.objects.create(
            attendance=self.attendance,
            title='Homework 1',
            description='Complete exercises 1-5',
        )
        self.form = EmploymentForm.objects.create(
            student=self.user,
            organ='Company ABC',
            status='در انتظار بررسی',
        )

    def test_user_creation(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_classes_creation(self):
        classes_count = Classes.objects.count()
        self.assertEqual(classes_count, 1)



  
# regression test for models:
class ModelRegressionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.grade = Grade.objects.create(name='Grade 1')
        self.major = Major.objects.create(name='Math')
        self.classes = Classes.objects.create(
            name='Class A',
            code='101',
            grade=self.grade,
            major=self.major,
        )
        self.book = Books.objects.create(
            name='Math Book',
            units=3,
            grade=self.grade,
        )
        self.attendance = Attendance.objects.create(
            attendance_class=self.classes,
            book=self.book,
            date='1400-01-01',
        )
        self.assign = Assign.objects.create(
            attendance=self.attendance,
            student=self.user,
            attendance_status='حاضر',
        )
        self.report_card = ReportCard.objects.create(
            student=self.user,
            report_card='This is a sample report card.',
        )
        self.homework = HomeWork.objects.create(
            attendance=self.attendance,
            title='Homework 1',
            description='Complete exercises 1-5',
        )
        self.form = EmploymentForm.objects.create(
            student=self.user,
            organ='Company ABC',
            status='در انتظار بررسی',
        )

    def test_assign_attendance_status(self):
        # Test that the attendance_status field in Assign model is one of the choices
        valid_statuses = [choice[0] for choice in Assign.ATTENDANCE_STATUS]
        self.assertIn(self.assign.attendance_status, valid_statuses)

    # Add more regression tests for specific model behaviors or conditions


# unit test for urls:
class ManagerUrlsTestCase(TestCase):
    def test_manager_panel_url(self):
        url = reverse('manager:manager_panel')
        self.assertEqual(url, '/manager/')

    def test_calendar_url(self):
        url = reverse('manager:calendar')
        self.assertEqual(url, '/manager/calendar/')

    def test_add_event_url(self):
        url = reverse('manager:add_event')
        self.assertEqual(url, '/manager/add-event/')

    def test_add_external_event_url(self):
        url = reverse('manager:add_external_event')
        self.assertEqual(url, '/manager/add-ex-event/')

    def test_update_event_url(self):
        url = reverse('manager:update_event')
        self.assertEqual(url, '/manager/update-event/')

    def test_update_event_desc_url(self):
        url = reverse('manager:update_event_desc')
        self.assertEqual(url, '/manager/update-event-desc/')

    def test_delete_event_url(self):
        url = reverse('manager:delete_event')
        self.assertEqual(url, '/manager/delete-event/')

    def test_delete_ex_event_url(self):
        url = reverse('manager:delete_ex_event')
        self.assertEqual(url, '/manager/delete-ex-event/')

    # Add more test methods for other URLs...

    def test_password_change_url(self):
        url = reverse('manager:user_password', args=[1])  # Replace 1 with a valid user ID
        self.assertEqual(url, '/manager/user/1/password/')



# unit test for filters:
class FiltersTestCase(TestCase):
    def setUp(self):
        # Create some test data for filtering
        self.student1 = User.objects.create(username='john', first_name='John', last_name='Doe', is_student=True, is_active=True, national_code='21312312')
        self.student2 = User.objects.create(username='alice', first_name='Alice', last_name='Smith', is_student=True, is_active=True, national_code='213123122')
        self.parent = User.objects.create(username='bob', first_name='Bob', last_name='Johnson', is_parent=True, is_active=True, national_code='213123112')
        self.teacher = User.objects.create(username='jane', first_name='Jane', last_name='Brown', is_teacher=True, is_active=True, national_code='21312412')

        self.class1 = Classes.objects.create(name='Class A', grade=None, major=None)
        self.class2 = Classes.objects.create(name='Class B', grade=None, major=None)

        self.emp_form1 = EmploymentForm.objects.create(student=self.student1, status='در انتظار بررسی')
        self.emp_form2 = EmploymentForm.objects.create(student=self.student2, status='بررسی شده')

        quiz_book = Books.objects.create(name='test', units=3)
        self.quiz1 = Quiz.objects.create(quiz_class=self.class1, name='Quiz A', time=3, quiz_book=quiz_book)
        self.quiz2 = Quiz.objects.create(quiz_class=self.class2, name='Quiz B', time=4, quiz_book=quiz_book)

    def test_student_filter(self):
        # Test the StudentFilter with the full_name filter
        data = {'full_name': 'John'}
        filter_set = StudentFilter(data, queryset=User.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs[0], self.student1)

    def test_parent_filter(self):
        # Test the ParentFilter with the full_name filter
        data = {'full_name': 'Bob'}
        filter_set = ParentFilter(data, queryset=User.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs[0], self.parent)

    def test_teacher_filter(self):
        # Test the TeacherFilter with the full_name filter
        data = {'full_name': 'Jane'}
        filter_set = TeacherFilter(data, queryset=User.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs[0], self.teacher)

    def test_class_filter(self):
        # Test the ClassFilter with the name filter
        data = {'name': 'Class A'}
        filter_set = ClassFilter(data, queryset=Classes.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs[0], self.class1)

    def test_emp_form_filter(self):
        # Test the EMPFormFilter with the status filter
        data = {'status': 'بررسی شده'}
        filter_set = EMPFormFilter(data, queryset=EmploymentForm.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs[0], self.emp_form2)

    def test_quiz_list_filter(self):
        # Test the QuizListFilter with the name filter
        data = {'name': 'Quiz A'}
        filter_set = QuizListFilter(data, queryset=Quiz.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs[0], self.quiz1)

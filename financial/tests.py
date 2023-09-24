from django.test import TestCase
from .models import Financial
import time

# non functional test for models:
class ModelNonFunctionalTest(TestCase):

    def test_model_performance(self):
        # Create and save multiple instances of the Financial model
        start_time = time.time()
        for i in range(100):
            Financial.objects.create(card_number=f'1234-5678-9012-{i:04}')
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        # Assert that the time taken to create and save 100 instances is less than 1 second (adjust as needed)
        self.assertLess(elapsed_time, 1.0)

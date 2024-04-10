from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.common.models import Rating
from fit_diary.workouts.models import Workout
from tests.test_base import TestBase

UserModel = get_user_model()


class IndexViewTests(TestBase):

    def test_get_index_view__expect_200_with_context_with_workouts_ordered_by_rating(self):

        user = self._create_user(self.USER_DATA)
        user2 = self._create_user(self.SECOND_USER_DATA)

        workout1 = Workout.objects.create(name='Workout 1', user=user)
        workout2 = Workout.objects.create(name='Workout 2', user=user)

        Rating.objects.create(workout=workout1, score=5, user=user)
        Rating.objects.create(workout=workout1, score=3, user=user2)
        Rating.objects.create(workout=workout2, score=2, user=user)
        Rating.objects.create(workout=workout2, score=4, user=user2)

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        workouts_in_context = list(response.context['workouts'])
        expected_order = [workout1, workout2]

        self.assertEqual(workouts_in_context, expected_order)

        self.assertAlmostEqual(workouts_in_context[0].average_rating, 4)
        self.assertAlmostEqual(workouts_in_context[1].average_rating, 3)

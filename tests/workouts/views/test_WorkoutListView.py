from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.workouts.models import Workout, Category, WorkoutType, Intensity
from tests.test_base import TestBase

UserModel = get_user_model()


class WorkoutListViewTestCase(TestBase):

    def setUp(self):
        self.user = self._create_user(self.USER_DATA)
        self.client.login(**self.USER_DATA)

    def test_filter_workouts_by_category_and_type(self):
        Workout.objects.create(name='Cardio 1', category=Category.ADVANCED, type=WorkoutType.HIIT,
                               intensity=Intensity.HIGH, user=self.user)
        Workout.objects.create(name='Strength Training 1', category=Category.BEGINNER,
                               type=WorkoutType.STRENGTH_TRAINING, intensity=Intensity.MEDIUM, user=self.user)
        response = self.client.get(reverse('list-workout'), {'category': Category.ADVANCED, 'type': WorkoutType.HIIT})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['workouts']), 1)
        self.assertEqual(response.context['workouts'][0].name, 'Cardio 1')
        self.assertEqual(response.context['total_workouts'](), 1)

    def test_sort_workouts_a_z(self):
        Workout.objects.create(name='Workout A', category=Category.BEGINNER, type=WorkoutType.HIIT,
                               intensity=Intensity.HIGH, user=self.user)
        Workout.objects.create(name='Workout Z', category=Category.ADVANCED,
                               type=WorkoutType.STRENGTH_TRAINING, intensity=Intensity.MEDIUM, user=self.user)

        response = self.client.get(reverse('list-workout'), {'sort': 'a_z'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'][0].name, 'Workout A')
        self.assertEqual(response.context['object_list'][1].name, 'Workout Z')

    def test_sort_workouts_z_a(self):
        Workout.objects.create(name='Workout A', category=Category.BEGINNER, type=WorkoutType.HIIT,
                               intensity=Intensity.HIGH, user=self.user)
        Workout.objects.create(name='Workout Z', category=Category.ADVANCED,
                               type=WorkoutType.STRENGTH_TRAINING, intensity=Intensity.MEDIUM, user=self.user)

        response = self.client.get(reverse('list-workout'), {'sort': 'z_a'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['workouts'][0].name, 'Workout Z')
        self.assertEqual(response.context['workouts'][1].name, 'Workout A')
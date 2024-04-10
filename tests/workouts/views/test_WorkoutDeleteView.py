from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.workouts.models import Workout
from tests.test_base import TestBase

UserModel = get_user_model()


class WorkoutDeleteViewTestCase(TestBase):

    def setUp(self):
        self.owner = self._create_user(self.USER_DATA)
        self.non_owner = self._create_user(self.SECOND_USER_DATA)
        self.workout = self._create_workout(self.owner)
        self.url = reverse('delete-workout', kwargs={'pk': self.workout.id})
        self.login_url = reverse('login-user')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    def test_forbidden_if_not_owner(self):
        self.client.login(**self.SECOND_USER_DATA)
        response = self.client.post(self.url)
        print(response)
        self.assertEqual(response.status_code, 403)

    def test_successful_deletion_by_owner(self):
        self.client.login(**self.USER_DATA)
        post_data = {
            'name': self.WORKOUT_DATA.get('name', None),
        }
        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, reverse('list-workout'))
        self.assertFalse(Workout.objects.filter(pk=self.workout.pk).exists())

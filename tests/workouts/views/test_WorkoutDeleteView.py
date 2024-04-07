from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.workouts.models import Workout

UserModel = get_user_model()


class WorkoutDeleteViewTestCase(TestCase):

    def setUp(self):
        self.owner = UserModel.objects.create_user(email='owner@example.com', password='testpass123')
        self.non_owner = UserModel.objects.create_user(email='nonowner@example.com', password='testpass456')
        self.workout = Workout.objects.create(name='Owner Workout', user=self.owner)
        self.url = reverse('delete-workout', kwargs={'pk': self.workout.id})
        self.login_url = reverse('login-user')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    def test_forbidden_if_not_owner(self):
        self.client.login(email='nonowner@example.com', password='testpass456')
        response = self.client.post(self.url)
        print(response)
        self.assertEqual(response.status_code, 403)

    def test_successful_deletion_by_owner(self):
        self.client.login(email='owner@example.com', password='testpass123')
        post_data = {
            'name': 'Owner Workout',
        }
        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, reverse('list-workout'))
        self.assertFalse(Workout.objects.filter(pk=self.workout.pk).exists())

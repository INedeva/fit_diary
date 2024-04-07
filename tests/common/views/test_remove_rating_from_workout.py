from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.common.models import Rating
from fit_diary.workouts.models import Workout

UserModel = get_user_model()


class RatingRemovalTestCase(TestCase):

    def test_remove_rating_from_workout(self):
        user = UserModel.objects.create_user(email='testuser@abv.bg', password='123Password')
        self.client.login(email='testuser@abv.bg', password='123Password')

        workout = Workout.objects.create(name='Test Workout', user=user)
        Rating.objects.create(score=5, workout=workout, user=user)

        referer_url = reverse('details-workout', kwargs={'pk': workout.id})

        response = self.client.post(
            reverse('remove_rating', kwargs={'workout_id': workout.id}),
            **{'HTTP_REFERER': referer_url}
        )

        self.assertRedirects(response, f'{referer_url}#workout-{workout.id}')
        self.assertFalse(Rating.objects.filter(user=user, workout=workout).exists())


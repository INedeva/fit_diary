from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.common.models import Rating
from fit_diary.workouts.models import Workout
from tests.test_base import TestBase

UserModel = get_user_model()


class RatingRemovalTestCase(TestBase):

    def test_remove_rating_from_workout(self):
        user = self._create_user(self.USER_DATA)
        self.client.login(**self.USER_DATA)

        workout = self._create_workout(user)
        Rating.objects.create(score=5, workout=workout, user=user)

        referer_url = reverse('details-workout', kwargs={'pk': workout.id})

        response = self.client.post(
            reverse('remove_rating', kwargs={'workout_id': workout.id}),
            **{'HTTP_REFERER': referer_url}
        )

        self.assertRedirects(response, f'{referer_url}#workout-{workout.id}')
        self.assertFalse(Rating.objects.filter(user=user, workout=workout).exists())


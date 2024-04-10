from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.common.models import Comment
from fit_diary.workouts.models import Workout
from tests.test_base import TestBase

UserModel = get_user_model()


class CommentCreationTestCase(TestBase):

    def test_create_comment_to_workout(self):

        # Create a user
        user = self._create_user(self.USER_DATA)
        self.client.login(**self.USER_DATA)

        # Create a workout
        workout = self._create_workout(user)
        comment_text = self.COMMENT_DATA.get('text', '')

        post_data = {
            'text': comment_text,
        }
        referer_url = reverse('details-workout', kwargs={'pk': workout.id})

        # Send a POST request
        response = self.client.post(
            reverse('comment', kwargs={'workout_id': workout.id}),
            post_data,
            **{'HTTP_REFERER': referer_url }
        )

        self.assertRedirects(response,  referer_url + f'#workout-{workout.id}')

        # Check that the Comment was created and is correct
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.text, comment_text)
        self.assertEqual(comment.user, user)
        self.assertEqual(comment.workout, workout)

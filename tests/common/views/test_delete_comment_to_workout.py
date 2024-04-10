from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.common.models import Comment
from fit_diary.workouts.models import Workout
from tests.test_base import TestBase

UserModel = get_user_model()


class CommentDeletionTestCase(TestBase):
    def test_post_owner__delete_comment_to_workout__succeed(self):
        user = self._create_user(self.USER_DATA)
        self.client.login(**self.USER_DATA)

        # Create a workout
        workout = self._create_workout(user)
        comment = self._create_comment(workout, user)

        referer_url = reverse(
            'details-workout',
            kwargs={'pk': workout.id}
        )

        # Send a POST request to delete the comment
        response = self.client.post(
            reverse('delete-comment-to-workout', kwargs={'workout_id': workout.id, 'comment_id': comment.id}),
            **{'HTTP_REFERER': referer_url}
        )

        # Verify the response redirects back to the workout detail page
        self.assertRedirects(response, f'{referer_url}#workout-{workout.id}')

        # Check that the Comment was indeed deleted
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_post_delete_comment__not_owner__fails(self):
        owner_user = self._create_user(self.USER_DATA)
        non_owner_user = self._create_user(self.SECOND_USER_DATA)

        workout = self._create_workout(owner_user)
        comment = self._create_comment(workout, owner_user)

        self.client.login(**self.SECOND_USER_DATA)

        referer_url = reverse(
            'details-workout', kwargs={'pk': workout.id})

        response = self.client.post(
            reverse('delete-comment-to-workout', kwargs={'workout_id': workout.id, 'comment_id': comment.id}),
            **{'HTTP_REFERER': referer_url}
        )

        self.assertRedirects(response, f'{referer_url}#workout-{workout.id}')
        # Verify the comment still exists
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())
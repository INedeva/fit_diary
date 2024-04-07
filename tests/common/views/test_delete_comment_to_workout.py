from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.common.models import Comment
from fit_diary.workouts.models import Workout

UserModel = get_user_model()


class CommentDeletionTestCase(TestCase):

    def test_post_owner__delete_comment_to_workout__succeed(self):
        user = UserModel.objects.create_user(email='testuser@abv.bg', password='123Password')
        self.client.login(email='testuser@abv.bg', password='123Password')

        # Create a workout
        workout = Workout.objects.create(name='Test Workout', user=user)
        comment = Comment.objects.create(text='Test Comment', workout=workout, user=user)

        referer_url = reverse('details-workout', kwargs={'pk': workout.id})

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
        owner_user = UserModel.objects.create_user(email='owner@abv.bg', password='123Password')
        non_owner_user = UserModel.objects.create_user(email='nonowner@abv.bg', password='123Password')

        workout = Workout.objects.create(name='Test Workout', user=owner_user)
        comment = Comment.objects.create(text='Test Comment', workout=workout, user=owner_user)

        self.client.login(email='nonowner@abv.bg', password='123Password')

        referer_url = reverse('details-workout', kwargs={'pk': workout.id})
        response = self.client.post(
            reverse('delete-comment-to-workout', kwargs={'workout_id': workout.id, 'comment_id': comment.id}),
            **{'HTTP_REFERER': referer_url}
        )

        self.assertRedirects(response, f'{referer_url}#workout-{workout.id}')
        # Verify the comment still exists
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())
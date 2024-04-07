from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from fit_diary.common.models import Comment
from fit_diary.workouts.models import Workout

UserModel = get_user_model()


class CommentCreationTestCase(TestCase):

    def test_create_comment_to_workout(self):

        # Create a user
        user = UserModel.objects.create_user(email='testuser@abv.bg', password='123Password')
        self.client.login(email='testuser@abv.bg', password='123Password')

        # Create a workout
        workout = Workout.objects.create(name='Test Workout', user=user)
        comment_text = 'This is a test comment.'

        post_data = {
            'text': comment_text,
        }
        referer_url = reverse('details-workout', kwargs={'pk': workout.id})

        # Send a POST request
        response = self.client.post(
            reverse('comment', kwargs={'workout_id': workout.id,}),
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

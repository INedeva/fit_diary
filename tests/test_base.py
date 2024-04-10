from django.contrib.auth import get_user_model
from django.test import TestCase

from fit_diary.common.models import Comment
from fit_diary.workouts.models import Workout

UserModel = get_user_model()


class TestBase(TestCase):

    USER_DATA = {
        "email": "testuser@abv.bg",
        "password": "TestPassword123",
    }
    SECOND_USER_DATA = {
        'email': 'nonowner@abv.bg',
        'password': '123Password'
    }

    WORKOUT_DATA = {
        'name': 'Test Workout'
    }

    COMMENT_DATA = {
        'text': 'This is a test comment.'
    }

    def _create_user(self, user_data):
        return UserModel.objects.create_user(**user_data)

    def _create_workout(self, user):
        return Workout.objects.create(**self.WORKOUT_DATA, user=user)

    def _create_comment(self, workout, user):
        return Comment.objects.create(**self.COMMENT_DATA, workout=workout, user=user)
from django.test import TestCase
from django.contrib.auth import get_user_model
from fit_diary.accounts.models import Profile
from tests.test_base import TestBase

UserModel = get_user_model()


class ProfileSignalTestCase(TestBase):
    def test_profile_creation(self):

        user = self._create_user(self.USER_DATA)

        self.assertIsNotNone(user)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.first()
        self.assertEqual(profile.user, user)


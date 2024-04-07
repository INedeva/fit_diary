from django.test import TestCase
from django.contrib.auth import get_user_model
from fit_diary.accounts.models import Profile

UserModel = get_user_model()


class ProfileSignalTestCase(TestCase):
    def test_profile_creation(self):

        user = UserModel.objects.create_user(email='testuser@abv.bg', password='12345')

        self.assertIsNotNone(user)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.first()
        self.assertEqual(profile.user, user)


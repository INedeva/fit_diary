from django.test import TestCase
from django.contrib.auth import get_user_model

from fit_diary.diary.models import MealEntry, DrinkEntry
from fit_diary.diary.views import calc_remaining_calories

UserModel = get_user_model()


class RemainingCaloriesCalculationTestCase(TestCase):

    def test_remaining_calories_calculation(self):

        user = UserModel.objects.create_user(email='testuser@abv.bg', password='123Password')
        user.profile.daily_calorie_goal = 2000
        user.profile.save()

        # Create meal and drink entries for today
        MealEntry.objects.create(user=user, name="Yogurt", calories=500)
        DrinkEntry.objects.create(user=user, name="Water", calories=100)

        remaining_calories = calc_remaining_calories(user)
        expected_remaining = 2000 - 600
        self.assertEqual(remaining_calories, expected_remaining)

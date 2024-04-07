from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry

UserModel = get_user_model()


class DiaryViewTestCase(TestCase):

    def setUp(self):
        user = UserModel.objects.create_user(email='testuser@abv.bg', password='123Password')
        self.client.login(email='testuser@abv.bg', password='123Password')

        self.meal = MealEntry.objects.create(user=user, name="Oatmeal", calories=300)
        DrinkEntry.objects.create(user=user, name="Orange Juice", calories=120)
        WaterIntakeEntry.objects.create(user=user, quantity=1.0, unit='Liters')


    def test_diary_view_today_entries(self):
        response = self.client.get(reverse('diary'), {'date_range': 'today'})

        self.assertEqual(response.status_code, 200)

        self.assertIn('meals', response.context)
        self.assertIn('drinks', response.context)
        self.assertIn('waters', response.context)

        self.assertEqual(len(response.context['meals']), 1)
        self.assertEqual(len(response.context['drinks']), 1)
        self.assertEqual(len(response.context['waters']), 1)

    def test_diary_view_meals_only(self):
        response = self.client.get(reverse('diary'), { 'log_type': 'meal'})

        self.assertEqual(response.status_code, 200)

        self.assertIn('meals', response.context)
        self.assertTrue(response.context['drinks'] is None)
        self.assertTrue(response.context['waters'] is None)

        self.assertEqual(len(response.context['meals']), 1)
        self.assertListEqual(
            list(response.context['meals']),
            [self.meal]
        )


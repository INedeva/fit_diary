from django.test import TestCase
from django.contrib.auth import get_user_model

from fit_diary.diary.models import WaterIntakeEntry, Unit
from fit_diary.diary.views import calc_water_consumption_in_liters
from tests.test_base import TestBase

UserModel = get_user_model()


class WaterConsumptionTestCase(TestBase):

    def test_calc_water_consumption_in_liters(self):
        user = self._create_user(self.USER_DATA)

        WaterIntakeEntry.objects.create(user=user, quantity=1.5, unit=Unit.LITERS)
        WaterIntakeEntry.objects.create(user=user, quantity=2.0, unit=Unit.LITERS)

        total_water_consumed = calc_water_consumption_in_liters(user)
        expected_total = 3.5
        self.assertEqual(total_water_consumed, expected_total)

from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class MealType(models.TextChoices):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'
    SNACK = 'Snack'


class Unit(models.TextChoices):
    GRAMS = 'Grams'
    MILLILITERS = 'Milliliters'
    PIECES = 'Pieces'
    KILOGRAMS = 'Kilograms'
    LITERS = 'Liters'


class DiaryEntry(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class FoodEntry(DiaryEntry):
    # TODO: Make this FLOAT
    quantity = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    unit = models.CharField(
        max_length=20,
        choices=Unit.choices,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class MealEntry(FoodEntry):
    name = models.CharField(
        max_length=100,
    )
    meal_type = models.CharField(
        # TODO : Do not hardcode max-length
        max_length=20,
        choices=MealType.choices,
        default=MealType.BREAKFAST,
    )
    calories = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
    )

    # TODO: To overwrite the default __str__method for all models


class DrinkEntry(FoodEntry):
    name = models.CharField(
        max_length=100,
    )
    calories = models.IntegerField(
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
    )

    # TODO: To overwrite the default __str__method for all models


class WaterIntakeEntry(FoodEntry):
    unit = models.CharField(
        max_length=20,
        choices=((Unit.LITERS, Unit.LITERS),),
    )

    # TODO: To overwrite the default __str__method for all models
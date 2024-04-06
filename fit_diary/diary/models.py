from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
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
    MAX_UNIT_LENGTH = max(len(x) for _, x in Unit.choices)

    quantity = models.FloatField(
        validators=[
            MinValueValidator(0.0, message="Quantity must be at least 0."),
        ],
        blank=True,
        null=True,
    )
    unit = models.CharField(
        max_length=MAX_UNIT_LENGTH,
        choices=Unit.choices,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class MealEntry(FoodEntry):
    MAX_NAME_LENGTH = 100
    MAX_MEAL_TYPE_LENGTH = max(len(x) for _, x in MealType.choices)

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )
    meal_type = models.CharField(
        max_length=MAX_MEAL_TYPE_LENGTH,
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
    unit = models.CharField(
        max_length=FoodEntry.MAX_UNIT_LENGTH,
        choices=Unit.choices,
        blank=True,
        null=True,
        default=Unit.GRAMS,
    )

    class Meta:
        verbose_name_plural = "Meal Entries"

    def __str__(self):
        return f"{self.name} ({self.meal_type}){(', calories: ' + str(self.calories)) if self.calories else ''}"


class DrinkEntry(FoodEntry):
    name = models.CharField(
        max_length=100,
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
    unit = models.CharField(
        max_length=FoodEntry.MAX_UNIT_LENGTH,
        choices=Unit.choices,
        blank=True,
        null=True,
        default=Unit.MILLILITERS,
    )

    class Meta:
        verbose_name_plural = "Drink Entries"

    def __str__(self):
        return f"{self.name}{(', calories: ' + str(self.calories)) if self.calories else ''}"


class WaterIntakeEntry(FoodEntry):
    unit = models.CharField(
        max_length=FoodEntry.MAX_UNIT_LENGTH,
        choices=((Unit.LITERS, Unit.LITERS),),
    )

    class Meta:
        verbose_name_plural = "Water Intake Entries"

    def __str__(self):
        return f"Water Intake: {self.quantity}{self.unit}"
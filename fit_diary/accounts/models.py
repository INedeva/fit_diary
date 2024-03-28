from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

from fit_diary.accounts.managers import FitDiaryUserManager
# TODO: extra validation everywhere


class FitDiaryUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            "unique": _("TA user with that email already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = FitDiaryUserManager()
    USERNAME_FIELD = "email"


class FitnessGoals(models.TextChoices):
    LOSE_WEIGHT = 'Lose weight'
    GAIN_MUSCLE = 'Gain muscle'
    BUILD_ENDURANCE = 'Build endurance'
    IMPROVE_FLEXIBILITY = 'Improve flexibility'
    INCREASE_STRENGTH = 'Increase strength'


class ActivityLevel(models.TextChoices):
    SEDENTARY = 'Sedentary'
    LIGHTLY_ACTIVE = 'Lightly Active'
    MODERATELY_ACTIVE = 'Moderately Active'
    VERY_ACTIVE = 'Very Active'
    EXTRA_ACTIVE = 'Extra Active'


class DietaryRestrictions(models.TextChoices):
    NONE = 'None'
    GLUTEN_FREE = 'Gluten-Free'
    DAIRY_FREE = 'Dairy-Free'
    NUT_FREE = 'Nut-Free'
    SUGAR_FREE = 'Sugar-Free'


class PreferredDiet(models.TextChoices):
    BALANCED = 'Balanced'
    HIGH_PROTEIN = 'High-Protein'
    LOW_CARB = 'Low-Carb'
    VEGAN = 'Vegan'
    VEGETARIAN = 'Vegetarian'
    KETO = 'Keto'


class Profile(models.Model):
    MAX_FIRST_NAME_LENGTH = 30
    MAX_LAST_NAME_LENGTH = 30
    MAX_FITNESS_GOALS_LENGTH = 50
    MAX_ACTIVITY_LEVEL_LENGTH = 50
    MAX_DIETARY_RESTRICTIONS_LENGTH = 15
    MAX_PREFERRED_DIET_LENGTH = 15

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='images/profile_pictures/',
        blank=True,
        null=True,
    )

    facebook_profile_url = models.URLField(
        blank=True,
        null=True,
        unique=True,
    )

    instagram_profile_url = models.URLField(
        blank=True,
        null=True,
        unique=True,
    )

    linkedin_profile_url = models.URLField(
        blank=True,
        null=True,
        unique=True,
    )

    fitness_goals = models.CharField(
        max_length=MAX_FITNESS_GOALS_LENGTH,
        choices=FitnessGoals.choices,
        blank=True,
        null=True,
        help_text='Your primary fitness goal'
    )

    goal_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Goal weight in kilograms',
        null=True,
        blank=True,
    )

    daily_calorie_goal = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    activity_level = models.CharField(
        max_length=MAX_ACTIVITY_LEVEL_LENGTH,
        choices=ActivityLevel.choices,
        blank=True,
        null=True
    )

    dietary_restrictions = models.CharField(
        max_length=MAX_DIETARY_RESTRICTIONS_LENGTH,
        choices=DietaryRestrictions.choices,
        help_text='Any health restrictions',
        blank=True,
        default='None',
    )

    preferred_diet = models.CharField(
        max_length=MAX_PREFERRED_DIET_LENGTH,
        choices=PreferredDiet.choices,
        blank=True,
        null=True,
        default='Balanced',
    )

    user = models.OneToOneField(
        FitDiaryUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.first_name or self.last_name

#
# class UserMeasurements(models.Model):
#     # TODO: Add validation for all fields to be positive
#     weight_kg = models.FloatField(
#         null=True,
#         blank=True,
#     )
#
#     height_cm = models.FloatField(
#         null=True,
#         blank=True,
#     )
#
#     biceps_cm = models.FloatField(
#         null=True,
#         blank=True,
#     )
#
#     chest_cm = models.FloatField(
#         null=True,
#         blank=True,
#     )
#
#     waist_cm = models.FloatField(
#         null=True,
#         blank=True,
#     )
#
#     hips_cm = models.FloatField(
#         null=True,
#         blank=True
#     )
#
#     thigh_cm = models.FloatField(
#         null=True,
#         blank=True
#     )
#
#     user = models.OneToOneField(
#         FitDiaryUser,
#         on_delete=models.CASCADE,
#     )
#
#     date = models.DateField(
#         auto_now_add=True,
#     )
#
#     # Body Adiposity Index (BAI)
#     # Underweight: BAI < 18
#     # Normal Weight: BAI = 18–25
#     # Overweight: BAI = 25–30
#     # Obese: BAI > 30
#     @property
#     def bai(self):
#         if self.height_cm and self.hips_cm:
#             height_m = self.height_cm / 100.0
#             bai = (self.hips_cm / (height_m ** 1.5)) - 18
#             return round(bai, 2)
#         return None

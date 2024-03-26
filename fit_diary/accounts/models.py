from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

from fit_diary.accounts.managers import FitDiaryUserManager


# Create your models here.

class FitDiaryUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            "unique":_("TA user with that email already exists."),
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

# TODO: to fix text choices


class Profile(models.Model):
    MAX_FIRST_NAME_LENGTH = 30
    MAX_LAST_NAME_LENGTH = 30
    MAX_GENDER_LENGTH = 20
    MAX_FITNESS_GOALS_LENGTH = 50
    MAX_ACTIVITY_LEVEL_LENGTH = 50
    MAX_DIETARY_RESTRICTIONS_LENGTH = 100
    MAX_PREFERRED_DIET_LENGTH = 50

    GENDERS = (
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
    )

    FITNESS_GOALS = (
        ('Lose weight', 'Lose weight'),
        ('Gain muscle', 'Gain muscle'),
        ('Build endurance', 'Build endurance'),
        ('Improve flexibility', 'Improve flexibility'),
        ('Increase strength', 'Increase strength'),
    )
    ACTIVITY_LEVEL = (
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderately Active', 'Moderately Active'),
        ('Very Active', 'Very Active'),
        ('Extra Active', 'Extra Active')
    )

    DIETARY_RESTRICTIONS = (
        ('None', 'None'),
        ('Gluten-Free', 'Gluten-Free'),
        ('Dairy-Free', 'Dairy-Free'),
        ('Nut-Free', 'Nut-Free'),
        ('Sugar-Free', 'Sugar-Free'),
    )

    PREFERRED_DIET = (
        ('Balanced', 'Balanced'),
        ('High-Protein', 'High-Protein'),
        ('Low-Carb', 'Low-Carb'),
        ('Vegan', 'Vegan'),
        ('Vegetarian', 'Vegetarian'),
        ('Keto', 'Keto')
    )

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

    gender = models.CharField(
        max_length=MAX_GENDER_LENGTH,
        choices=GENDERS,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='images/',
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
        choices=FITNESS_GOALS,
        blank=True,
        null=True,
        help_text='Your primary fitness goal')

    goal_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Goal weight in kilograms',
        null=True,
        blank=True,
    )

    activity_level = models.CharField(
        max_length=MAX_ACTIVITY_LEVEL_LENGTH,
        choices=ACTIVITY_LEVEL,
        blank=True,
        null=True
    )

    dietary_restrictions = models.CharField(
        max_length=MAX_DIETARY_RESTRICTIONS_LENGTH,
        choices=DIETARY_RESTRICTIONS,
        help_text='Any health restrictions',
        blank=True,
        default='None',
    )

    preferred_diet = models.CharField(
        max_length=MAX_PREFERRED_DIET_LENGTH,
        choices=PREFERRED_DIET,
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

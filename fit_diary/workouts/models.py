from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

UserModel = get_user_model()


class Category(models.TextChoices):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'


class Intensity(models.TextChoices):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


class WorkoutType(models.TextChoices):
    CARDIO = 'Cardio'
    STRENGTH_TRAINING = 'Strength Training'
    HIIT = 'High-Intensity Interval Training'
    FLEXIBILITY = 'Flexibility'
    GROUP_CLASSES = 'Group Classes'


class Workout(models.Model):

    name = models.CharField(
        max_length=100
    )

    video_url = models.URLField(
        null=True,
        blank=True,
    )

    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.BEGINNER,
        null=True,
        blank=True,
    )

    intensity = models.CharField(
        max_length=50,
        choices=Intensity.choices,
        default=Intensity.LOW,
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=50,
        choices=WorkoutType.choices,
        default=WorkoutType.STRENGTH_TRAINING,
        null=True,
        blank=True,
    )

    equipment_needed = models.CharField(
        max_length=100,
        help_text="List of equipment needed",
        null=True,
        blank=True,

    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

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
    MAX_NAME_LENGTH = 100
    MAX_EQUIPMENT_NEEDED_LENGTH = 100

    MAX_CATEGORY_LENGTH = max(len(x) for _, x in Category.choices)
    MAX_INTENSITY_LENGTH = max(len(x) for _, x in Intensity.choices)
    # FIXME: having issues with MAX_TYPE_LENGTH = max(len(x) for _, x in WorkoutType.choices)
    # ERROR: workouts.Workout.type: (fields.E009) 'max_length' is too small to fit the longest value in 'choices' (32 characters).
    MAX_TYPE_LENGTH = 50

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        help_text="Name of the exercise"
    )

    video_url = models.URLField(
        null=True,
        blank=True,
        help_text="Provide a URL to a video demonstration of the workout."
    )

    category = models.CharField(
        max_length=MAX_CATEGORY_LENGTH,
        choices=Category.choices,
        default=Category.BEGINNER,
        null=True,
        blank=True,
        help_text="Select the skill level category."
    )

    intensity = models.CharField(
        max_length=MAX_INTENSITY_LENGTH,
        choices=Intensity.choices,
        default=Intensity.LOW,
        null=True,
        blank=True,
        help_text="Choose the intensity level of the workout."
    )

    type = models.CharField(
        max_length=MAX_TYPE_LENGTH,
        choices=WorkoutType.choices,
        default=WorkoutType.STRENGTH_TRAINING,
        null=True,
        blank=True,
        help_text="Select the type of workout. For example, Cardio, Strength Training, or HIIT."
    )

    equipment_needed = models.CharField(
        max_length=MAX_EQUIPMENT_NEEDED_LENGTH,
        help_text="List any specific equipment needed for the workout. Leave blank if no equipment is necessary.",
        null=True,
        blank=True,

    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="Provide a brief description of the workout."
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


    def __str__(self):
        return f"{self.name} - {self.type}, ({self.intensity})"
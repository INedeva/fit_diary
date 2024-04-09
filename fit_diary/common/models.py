from django.contrib.auth import get_user_model
from django.db import models

from fit_diary.workouts.models import Workout

UserModel = get_user_model()


class Comment(models.Model):

    MAX_TEXT_LENGTH = 500

    text = models.TextField(
        max_length=MAX_TEXT_LENGTH,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.profile.full_name}: {self.text[:10]}... ({self.created_at.strftime('%Y-%m-%d')})"


class Rating(models.Model):

    score = models.IntegerField(
        default=1, choices=[(i, i) for i in range(1, 6)], verbose_name='rating'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (('user', 'workout'),)
        index_together = (('user', 'workout'),)

    def __str__(self):
        return f"{self.user.profile.full_name} rated {self.workout.name} with {self.score}"

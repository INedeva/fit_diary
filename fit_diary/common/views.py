from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from fit_diary.common.forms import AddCommentForm
from fit_diary.common.models import Rating, Comment
from fit_diary.workouts.models import Workout


def index(request):

    # Get top 10 highest rated workouts
    queryset = Workout.objects.annotate(average_rating=Avg('rating__score')).order_by('-average_rating')[:10]

    context = {'workouts': queryset}
    return render(request, 'common/index.html', context)


def about(request):
    return render(request, 'common/about.html')


def contacts(request):
    return render(request, 'common/contacts.html')


@login_required
def create_comment_to_workout(request, workout_id):

    if request.method == 'POST':
        workout = Workout.objects.get(id=workout_id)
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.workout = workout
            comment.user = request.user
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#workout-{workout_id}')

@login_required
def delete_comment_to_workout(request, workout_id, comment_id):
    comment = Comment.objects.filter(id=comment_id).first()

    if request.method == 'POST' and comment.workout.id == workout_id and comment.user == request.user:
        comment.delete()

    return redirect(request.META['HTTP_REFERER'] + f'#workout-{workout_id}')


@login_required
def remove_rating_from_workout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    Rating.objects.filter(user=request.user, workout=workout).delete()
    return redirect(request.META['HTTP_REFERER'] + f'#workout-{workout.pk}')
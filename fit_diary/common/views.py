from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from fit_diary.common.forms import AddCommentForm
from fit_diary.common.models import Rating, Comment
from fit_diary.workouts.models import Workout


# Create your views here.


def index(request):
    queryset = Workout.objects.all()

    context = {'workouts': queryset}
    return render(request, 'common/index.html', context)


def about(request):
    return render(request, 'common/about.html')


def contacts(request):
    return render(request, 'common/contacts.html')

@login_required
def create_comment_to_workout(request, workout_id):
    # TODO: number of comments per workout
    if request.method == 'POST':
        workout = Workout.objects.get(id=workout_id)
        form = AddCommentForm(request.POST)
        print(form.is_valid())
        print(form.cleaned_data)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.workout = workout
            comment.user = request.user
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#workout-{workout_id}')

@login_required
def delete_comment_to_workout(request, workout_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, workout=workout_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
    #     messages.success(request, "Your comment has been deleted.")
    # else:
    #     messages.error(request, "Invalid request.")
    return redirect(request.META['HTTP_REFERER'] + f'#workout-{workout_id}')

@login_required
def remove_rating_from_workout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    Rating.objects.filter(user=request.user, workout=workout).delete()
    return redirect(request.META['HTTP_REFERER'] + f'#workout-{workout.pk}')
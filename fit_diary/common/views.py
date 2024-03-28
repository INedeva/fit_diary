from django.shortcuts import render

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

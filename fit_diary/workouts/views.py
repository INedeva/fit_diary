from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from fit_diary.workouts.forms import WorkoutDeleteForm
from fit_diary.workouts.models import Workout, Category, Intensity, WorkoutType


# Create your views here.


class WorkoutCreateView(CreateView):
    model = Workout
    fields = "__all__"
    template_name = 'workouts/create-workout.html'
    success_url = reverse_lazy('index')  # TODO: fix url


class WorkoutEditView(UpdateView):
    model = Workout
    fields = "__all__"
    template_name = 'workouts/edit-workout.html'
    success_url = reverse_lazy('index')  # TODO: fix url


class WorkoutListView(ListView):
    model = Workout
    context_object_name = 'workouts'
    template_name = 'workouts/catalogue-workouts.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category', '')
        type = self.request.GET.get('type', '')
        intensity = self.request.GET.get('intensity', '')
        sort = self.request.GET.get('sort', '')

        if category:
            queryset = queryset.filter(category=category)

        if type:
            queryset = queryset.filter(type=type)

        if intensity:
            queryset = queryset.filter(intensity=intensity)

        # TODO: to make it sort by date instead of id
        if sort == 'oldest':
            queryset = queryset.order_by('id')
        elif sort == 'newest':
            queryset = queryset.order_by('-id')
        elif sort == 'a_z':
            # TODO: Check why names is not working as expected - maybe ASCII - lower/upper case ?
            queryset = queryset.order_by('name')
        elif sort == 'z_a':
            queryset = queryset.order_by('-name')

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['total_workouts'] = self.get_queryset().count
        context['category_choices'] = Category.choices
        context['intensity_choices'] = Intensity.choices
        context['workout_type_choices'] = WorkoutType.choices

        return context


class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workouts/details-workout.html'


class WorkoutDeleteView(DeleteView):
    model = Workout
    form_class = WorkoutDeleteForm

    template_name = 'workouts/delete-workout.html'
    success_url = reverse_lazy('index')   # TODO: fix url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    # def delete(self, request, *args, **kwargs):
    #     workout = self.get_object()
    #     workout.delete()
    #     return redirect(self.success_url)
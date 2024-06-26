from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from fit_diary.common.forms import AddCommentForm, AddRatingForm
from fit_diary.common.models import Rating
from fit_diary.workouts.forms import WorkoutDeleteForm
from fit_diary.workouts.mixins import OwnerRequiredMixin
from fit_diary.workouts.models import Workout, Category, Intensity, WorkoutType


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    fields = ( 'name', 'video_url', 'category', 'intensity', 'type', 'equipment_needed', 'description')
    template_name = 'workouts/create-workout.html'
    success_url = reverse_lazy('list-workout')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.instance.user = self.request.user
        return form

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not self.request.user.groups.filter(name='Moderator').exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)



class WorkoutEditView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Workout
    fields = ('name', 'video_url', 'category', 'intensity', 'type', 'equipment_needed', 'description')
    template_name = 'workouts/edit-workout.html'
    success_url = reverse_lazy('list-workout')


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    context_object_name = 'workouts'
    template_name = 'workouts/catalogue-workouts.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category', '')
        type = self.request.GET.get('type', '')
        intensity = self.request.GET.get('intensity', '')
        sort = self.request.GET.get('sort', '')

        # Filtration
        if category:
            queryset = queryset.filter(category=category)

        if type:
            queryset = queryset.filter(type=type)

        if intensity:
            queryset = queryset.filter(intensity=intensity)

        # Sorting
        if sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'a_z':
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


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'workouts/details-workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = AddCommentForm()

        workout = context['object']
        user_rating = Rating.objects.filter(user=self.request.user, workout=workout).first()
        context['rating_form'] = AddRatingForm(instance=user_rating)

        average_rating = Rating.objects.filter(workout=workout).aggregate(Avg('score'))['score__avg']
        context['average_rating'] = round(average_rating or 0, 2)

        context['rating_range'] = range(5, 0, -1)
        return context

    def post(self, request, *args, **kwargs):
        workout = self.get_object()
        form = AddRatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                workout=workout,
                defaults={'score': form.cleaned_data['score']}
            )
            return redirect(request.META['HTTP_REFERER'] + f'#workout-{workout.pk}')


class WorkoutDeleteView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Workout
    form_class = WorkoutDeleteForm

    template_name = 'workouts/delete-workout.html'
    success_url = reverse_lazy('list-workout')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs


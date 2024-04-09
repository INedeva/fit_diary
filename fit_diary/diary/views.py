from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, Q, Sum
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db import models

from fit_diary.diary.forms import MealEntryForm, DrinkEntryForm, WaterIntakeEntryForm, MealEntryDeleteForm, \
    DrinkEntryDeleteForm, WaterIntakeEntryDeleteForm
from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry
from fit_diary.workouts.mixins import OwnerRequiredMixin


class DiaryEntryMappingMixin:
    models_mapping = {
        'meal': MealEntry,
        'drink': DrinkEntry,
        'water': WaterIntakeEntry,
    }
    forms_mapping = {
        'meal': MealEntryForm,
        'drink': DrinkEntryForm,
        'water': WaterIntakeEntryForm,
    }
    delete_forms_mapping = {
        'meal': MealEntryDeleteForm,
        'drink': DrinkEntryDeleteForm,
        'water': WaterIntakeEntryDeleteForm,
    }

    def get_form_class(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)

        if entry_type not in self.forms_mapping:
            raise Http404("Entry type not found")

        return self.forms_mapping[entry_type]

    def get_model(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)

        if entry_type not in self.models_mapping:
            raise Http404("Model not found")

        return self.models_mapping[entry_type]


class DiaryEntryCreateView(DiaryEntryMappingMixin, LoginRequiredMixin, CreateView):
    template_name = 'diary/create-diary-record.html'
    success_url = reverse_lazy('diary')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.instance.user = self.request.user
        return form

    def get_queryset(self):
        return self.get_model().objects.all()


class DiaryEntryEditView(OwnerRequiredMixin, DiaryEntryMappingMixin, LoginRequiredMixin, UpdateView):
    template_name = 'diary/edit-diary-record.html'
    success_url = reverse_lazy('diary')

    def get_queryset(self):
        return self.get_model().objects.all()


class DiaryEntryDeleteView(OwnerRequiredMixin, DiaryEntryMappingMixin, LoginRequiredMixin, DeleteView):
    template_name = 'diary/delete-diary-record.html'
    success_url = reverse_lazy('diary')

    def get_form_class(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)
        if entry_type not in DiaryEntryMappingMixin.delete_forms_mapping:
            raise Http404("Entry type not found")
        else:
            return DiaryEntryMappingMixin.delete_forms_mapping[entry_type]

    def get_queryset(self):
        return self.get_model().objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs


def calc_remaining_calories(user):
    DEFAULT_CALORIE_GOAL = 2000

    total_calories = 0

    date_query = Q(created_at__date=now().date())
    log_type_query = Q(user=user)

    meals = MealEntry.objects.filter(log_type_query & date_query)
    drinks = DrinkEntry.objects.filter(log_type_query & date_query)

    if meals:
        total_calories += meals.aggregate(total_calories=Coalesce(Sum('calories'), 0))['total_calories']

    if drinks:
        # Coalesce() is a Django function that returns the first non - null expression among its arguments.
        # In this context, Coalesce() ensures that even if there are no entries
        # for meals, the expression doesn't return None, but instead returns 0.
        total_calories += drinks.aggregate(total_calories=Coalesce(Sum('calories'), 0))['total_calories']

    daily_goal = user.profile.daily_calorie_goal or DEFAULT_CALORIE_GOAL
    remaining_calories = daily_goal - total_calories

    return remaining_calories


def calc_water_consumption_in_liters(user):
    total_water = 0.0

    date_query = Q(created_at__date=now().date())
    log_type_query = Q(user=user)

    water = WaterIntakeEntry.objects.filter(log_type_query & date_query)

    if water:
        total_water += water.aggregate(total_water=Coalesce(Sum('quantity'), Value(0.0, output_field=models.FloatField())))['total_water']

    return total_water


@login_required
def diary_view(request):
    current_user = request.user

    remaining_calories = calc_remaining_calories(current_user)
    water_consumption = calc_water_consumption_in_liters(current_user)

    log_type = request.GET.get('log_type', '')
    date_range = request.GET.get('date_range', '')

    total_logs = 0

    meals = None
    drinks = None
    waters = None

    # Initialize query filters
    date_query = Q()
    log_type_query = Q(user=current_user)

    # Determine the date or date range for filtering
    if date_range == 'today':
        today = now().date()
        date_query &= Q(created_at__date=today)
    elif date_range == 'yesterday':
        yesterday = now().date() - timedelta(days=1)
        date_query &= Q(created_at__date=yesterday)
    elif date_range == 'last_week':
        last_week_start = now().date() - timedelta(days=7)
        last_week_end = now().date()
        date_query &= Q(created_at__date__range=(last_week_start, last_week_end))

    # extract the querysets if there is no filtration or filter is matching the type
    if log_type == 'meal' or not log_type:
        meals = MealEntry.objects.filter(log_type_query & date_query).annotate(
            entry_type=Value('meal', output_field=models.CharField())
        )
        if meals:
            total_logs += meals.count()

    if log_type == 'drink' or not log_type:
        drinks = DrinkEntry.objects.filter(log_type_query & date_query).annotate(
            entry_type=Value('drink', output_field=models.CharField())
        )
        if drinks:
            total_logs += drinks.count()

    if log_type == 'water' or not log_type:
        waters = WaterIntakeEntry.objects.filter(log_type_query & date_query).annotate(
            entry_type=Value('water', output_field=models.CharField())
        )
        if waters:
            total_logs += waters.count()

    context = {
        'meals': meals,
        'drinks': drinks,
        'waters': waters,
        'total_logs': total_logs,
        'remaining_calories': remaining_calories,
        'water_consumption': water_consumption,
    }

    return render(request, 'diary/diary.html', context)


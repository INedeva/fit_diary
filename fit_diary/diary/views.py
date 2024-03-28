from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, Q
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db import models

from fit_diary.diary.forms import MealEntryForm, DrinkEntryForm, WaterIntakeEntryForm, MealEntryDeleteForm, \
    DrinkEntryDeleteForm, WaterIntakeEntryDeleteForm
from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry


# TODO: add login required mixin
# class DiaryEntryCreateView(LoginRequiredMixin, CreateView):
class DiaryEntryCreateView(CreateView):
    template_name = 'diary/create-diary-record.html'
    success_url = reverse_lazy('diary')

    # TODO: to rework to optimize this in a dictionary
    def get_form_class(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)
        if entry_type == 'meal':
            return MealEntryForm
        elif entry_type == 'drink':
            return DrinkEntryForm
        elif entry_type == 'water':
            return WaterIntakeEntryForm
        else:
            raise Http404("Entry type not found")

    def get_model(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)
        if entry_type == 'meal':
            return MealEntry
        elif entry_type == 'drink':
            return DrinkEntry
        elif entry_type == 'water':
            return WaterIntakeEntry
        else:
            raise Http404("Model not found")

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        print(self.request.user)  # TODO: for debug - remove later
        form.instance.user = self.request.user
        return form

    def get_queryset(self):
        return self.get_model().objects.all()


# TODO: LoginRequiredMixin
class DiaryEntryEditView(UpdateView):
    template_name = 'diary/edit-diary-record.html'
    success_url = reverse_lazy('diary')

    def get_form_class(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)
        if entry_type == 'meal':
            return MealEntryForm
        elif entry_type == 'drink':
            return DrinkEntryForm
        elif entry_type == 'water':
            return WaterIntakeEntryForm
        else:
            raise Http404("Entry type not found")

    def get_model(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)
        if entry_type == 'meal':
            return MealEntry
        elif entry_type == 'drink':
            return DrinkEntry
        elif entry_type == 'water':
            return WaterIntakeEntry
        else:
            raise Http404("Model not found")

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=form_class)
    #     print(self.request.user)  # TODO: for debug - remove later
    #     form.instance.user = self.request.user
    #     return form

    # def get_object(self, queryset=None):
    #     pass

    def get_queryset(self):
        return self.get_model().objects.all()


# TODO: LoginRequiredMixin
class DiaryEntryDeleteView(DeleteView):
    template_name = 'diary/delete-diary-record.html'
    success_url = reverse_lazy('diary')

    def get_form_class(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)
        if entry_type == 'meal':
            return MealEntryDeleteForm
        elif entry_type == 'drink':
            return DrinkEntryDeleteForm
        elif entry_type == 'water':
            return WaterIntakeEntryDeleteForm
        else:
            raise Http404("Entry type not found")

    def get_model(self):
        entry_type = self.request.GET.get('entry_type', None) or self.request.POST.get('entry_type', None)
        if entry_type == 'meal':
            return MealEntry
        elif entry_type == 'drink':
            return DrinkEntry
        elif entry_type == 'water':
            return WaterIntakeEntry
        else:
            raise Http404("Model not found")

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=form_class)
    #     print(self.request.user)  # TODO: for debug - remove later
    #     form.instance.user = self.request.user
    #     return form

    # def get_object(self, queryset=None):
    #     pass

    def get_queryset(self):
        return self.get_model().objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs


# @login_required - TODO: add it later
def diary_view(request):
    current_user = request.user
    log_type = request.GET.get('log_type', '')
    date_range = request.GET.get('date_range', '')

    total_logs = 0

    meals = None
    drinks = None
    waters = None

    # Initialize query filters
    date_query = Q()
    log_type_query = Q(user=current_user)  # Default to filtering by current user only

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

    # extract the querysets
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
    }

    return render(request, 'diary/diary.html', context)


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.db import models

from fit_diary.diary.forms import MealEntryForm, DrinkEntryForm, WaterIntakeEntryForm
from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry


# Create your views here.
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
        print(self.request.user)  # TODO: for debuf - remove later
        form.instance.user = self.request.user
        return form

    def get_queryset(self):
        return self.get_model().objects.all()


# TODO: create CBV
# @login_required
# def diary_view(request):
#     return render(request, 'diary/diary.html')


# @login_required - TODO: add it later
def diary_view(request):
    current_user = request.user

    meals = MealEntry.objects.filter(user=current_user).annotate(
        entry_type=Value('meal', output_field=models.CharField()))
    # ).values_list(
    #     'id', 'created_at', 'name', 'photo',
    #     'meal_type', 'calories',
    #     'quantity', 'unit', 'entry_type',
    #     named=True
    # )

    drinks = DrinkEntry.objects.filter(user=current_user).annotate(
        entry_type=Value('drink', output_field=models.CharField())
    ).values_list(
        'id', 'created_at', 'name', 'photo',
        'calories',
        'quantity', 'unit', 'entry_type',
        named=True
    )

    waters = WaterIntakeEntry.objects.filter(user=current_user).annotate(
        entry_type=Value('water', output_field=models.CharField())
    ).values_list(
        'id', 'created_at',
        'quantity', 'unit', 'entry_type',
        named=True
    )

    context = {
        'meals': meals,
        'drinks': drinks,
        'waters': waters,
        'total_logs': meals.count() + drinks.count() + waters.count(),
    }

    return render(request, 'diary/diary.html', context)


# class DiaryView(ListView):
#     # TODO: Add Login required mixin
#     template_name = 'diary/diary.html'
#     paginate_by = 6
#
#     def get_queryset(self):
#         current_user = self.request.user
#         meals = MealEntry.objects.filter(user=current_user).annotate(
#             entry_type=Value('meal', output_field=models.CharField())
#             ).values_list(
#             'id', 'created_at', 'name', 'photo',
#             'meal_type', 'calories',
#             'quantity','unit', 'entry_type',
#             named=True
#         )
#
#         drinks = DrinkEntry.objects.filter(user=current_user).annotate(
#             entry_type=Value('drink', output_field=models.CharField())
#             ).values_list(
#             'id', 'created_at', 'name', 'photo',
#             'calories',
#             'quantity', 'unit', 'entry_type',
#             named=True
#         )
#
#         waters = WaterIntakeEntry.objects.filter(user=current_user).annotate(
#             entry_type=Value('water', output_field=models.CharField())
#             ).values_list(
#             'id', 'created_at',
#             'quantity', 'unit', 'entry_type',
#             named=True
#         )
#
#         combined_list = list(meals) + list(drinks) + list(waters)
#
#         sorted_combined_list = sorted(combined_list, key=lambda x: x.created_at, reverse=True)
#         return sorted_combined_list
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_logs'] = len(self.get_queryset())
#
#         return context



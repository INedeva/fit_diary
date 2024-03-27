from django import forms

from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry


class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        exclude = ('user',)
        fields = ['name', 'photo', 'meal_type', 'quantity', 'unit', 'calories']


class DrinkEntryForm(forms.ModelForm):
    class Meta:
        model = DrinkEntry
        exclude = ('user',)
        fields = ['name', 'photo', 'quantity', 'unit', 'calories']


class WaterIntakeEntryForm(forms.ModelForm):
    class Meta:
        model = WaterIntakeEntry
        exclude = ('user',)
        fields = ['quantity', 'unit']
from django import forms

from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry


class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        exclude = ('user',)
        fields = ['name', 'photo', 'meal_type', 'quantity', 'unit', 'calories', 'notes']


class DrinkEntryForm(forms.ModelForm):
    class Meta:
        model = DrinkEntry
        exclude = ('user',)
        fields = ['name', 'photo', 'quantity', 'unit', 'calories', 'notes']


class WaterIntakeEntryForm(forms.ModelForm):
    class Meta:
        model = WaterIntakeEntry
        exclude = ('user',)
        fields = ['quantity', 'unit', 'notes']


class MealEntryDeleteForm(MealEntryForm):
    class Meta(MealEntryForm.Meta):
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'meal_type': forms.Select(attrs={'readonly': True}),
            'quantity': forms.NumberInput(attrs={'readonly': True}),
            'unit': forms.Select(attrs={'readonly': True}),
            'calories': forms.NumberInput(attrs={'readonly': True}),
            'photo': forms.FileInput(attrs={'readonly': True}),
            'notes': forms.Textarea(attrs={'readonly': True}),
        }


class DrinkEntryDeleteForm(DrinkEntryForm):
    class Meta(DrinkEntryForm.Meta):
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'quantity': forms.NumberInput(attrs={'readonly': True}),
            'unit': forms.Select(attrs={'readonly': True}),
            'calories': forms.NumberInput(attrs={'readonly': True}),
            'photo': forms.FileInput(attrs={'readonly': True}),
            'notes': forms.Textarea(attrs={'readonly': True}),
        }


class WaterIntakeEntryDeleteForm(WaterIntakeEntryForm):
    class Meta(WaterIntakeEntryForm.Meta):
        widgets = {
            'quantity': forms.NumberInput(attrs={'readonly': True}),
            'unit': forms.Select(attrs={'readonly': True}),
            'notes': forms.Textarea(attrs={'readonly': True}),
        }


from django import forms

from fit_diary.workouts.models import Workout


class WorkoutDeleteForm(forms.ModelForm):
    # def save(self, commit=True):
    #     if commit:
    #         self.instance.delete()
    #     return self.instance

    class Meta:
        model = Workout
        fields = ['name', 'video_url', 'category', 'intensity', 'type', 'equipment_needed', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'video_url': forms.URLInput(attrs={'readonly': True}),
            'category': forms.Select(attrs={'readonly': True}),
            'intensity': forms.Select(attrs={'readonly': True}),
            'type': forms.Select(attrs={'readonly': True}),
            'equipment_needed': forms.TextInput(attrs={'readonly': True}),
            'description': forms.Textarea(attrs={'readonly': True}),
        }
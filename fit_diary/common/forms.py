from django import forms

from fit_diary.common.models import Comment, Rating


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add comment...'}),
        }

# TODO: edit and delete comments


class AddRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
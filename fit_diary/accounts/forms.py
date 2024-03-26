from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from fit_diary.accounts.models import Profile

UserModel = get_user_model()


class FitDiaryUserCreationForm(UserCreationForm):
    user = None

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class FitDiaryUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
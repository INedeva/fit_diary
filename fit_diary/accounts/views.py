from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from fit_diary.accounts.forms import FitDiaryUserCreationForm, ProfileEditForm
from fit_diary.accounts.models import Profile
from fit_diary.workouts.mixins import OwnerRequiredMixin

UserModel = get_user_model()


class LoginUserView(LoginView):
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('diary')


class RegisterUserView(CreateView):
    form_class = FitDiaryUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('diary')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request,  form.instance)
        return result


def logout_user(request):
    logout(request)
    return redirect('index')


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    queryset = Profile.objects.all().prefetch_related('user')
    template_name = 'accounts/details-profile.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    queryset = Profile.objects.all()
    form_class = ProfileEditForm
    template_name = 'accounts/edit-profile.html'

    def get_success_url(self):
        return reverse("details-profile", kwargs={"pk":self.object.pk,})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    # Deleting directly the user, to use the CASCADE, otherwise only Profile is deleted
    queryset = UserModel.objects.all()
    template_name = 'accounts/delete-profile.html'
    success_url = reverse_lazy('index')



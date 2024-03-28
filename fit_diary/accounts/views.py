from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from fit_diary.accounts.forms import FitDiaryUserCreationForm, ProfileEditForm
from fit_diary.accounts.models import Profile


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


class ProfileDetailsView(DetailView):
    queryset = Profile.objects.all().prefetch_related('user')
    template_name = 'accounts/details-profile.html'


class ProfileEditView(UpdateView):
    queryset = Profile.objects.all()
    form_class = ProfileEditForm
    template_name = 'accounts/edit-profile.html'

    def get_success_url(self):
        return reverse("details-profile", kwargs={"pk":self.object.pk,})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileDeleteView(DeleteView):
    queryset = Profile.objects.all()
    template_name = 'accounts/delete-profile.html'
    success_url = reverse_lazy('index')
    # TODO: to ask should not we delete the user not the profile ?
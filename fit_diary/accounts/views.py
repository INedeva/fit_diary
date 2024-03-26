from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from fit_diary.accounts.forms import FitDiaryUserCreationForm, ProfileEditForm
from fit_diary.accounts.models import Profile


# Create your views here.

# TODO: remove later
def index(request):
    return render(request, 'base.html')


class LoginUserView(LoginView):
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True


class RegisterUserView(CreateView):
    form_class = FitDiaryUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')

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

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=form_class)
    #     form.fields['date_of_birth'].widget.attrs['type'] = 'date'
    #     return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileDeleteView(DeleteView):
    queryset = Profile.objects.all()
    template_name = 'accounts/delete-profile.html'
    success_url = reverse_lazy('register-user')  # TODO: redirect to index ?
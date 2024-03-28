from django.urls import path, include

from fit_diary.accounts.views import RegisterUserView, LoginUserView, logout_user, ProfileDetailsView, \
    ProfileEditView, ProfileDeleteView

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('logout/', logout_user, name='logout-user'),

    path('profile/<int:pk>/', include([
            path('', ProfileDetailsView.as_view(), name='details-profile'),
            path('edit/', ProfileEditView.as_view(), name='edit-profile'),
            path('delete/', ProfileDeleteView.as_view(), name='delete-profile'),
        ])),
)
from django.urls import path, include

from fit_diary.workouts.views import WorkoutListView, WorkoutCreateView, WorkoutDetailView, WorkoutEditView, \
    WorkoutDeleteView

urlpatterns = (
    path("", WorkoutListView.as_view(), name="list-workout"),
    path("create/", WorkoutCreateView.as_view(), name="create-workout"),
    path('<int:pk>/', include([
                path('', WorkoutDetailView.as_view(), name='details-workout'),
                path('edit/', WorkoutEditView.as_view(), name='edit-workout'),
                path('delete/', WorkoutDeleteView.as_view(), name='delete-workout'),
            ])),


)



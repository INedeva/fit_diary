from django.urls import path

from fit_diary.common.views import index, about, contacts, create_comment_to_workout, remove_rating_from_workout, \
    delete_comment_to_workout

urlpatterns = (
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('workouts/<int:workout_id>/comment/', create_comment_to_workout, name='comment'),
    path('workouts/<int:workout_id>/comments/<int:comment_id>/delete/', delete_comment_to_workout, name='delete-comment-to-workout'),

    path('workout/<int:workout_id>/remove_rating/', remove_rating_from_workout, name='remove_rating'),

)



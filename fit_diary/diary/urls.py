from django.urls import path, include

from fit_diary.diary.views import DiaryEntryCreateView, diary_view, DiaryEntryEditView, DiaryEntryDeleteView

urlpatterns = (
    path('', diary_view, name='diary'),
    path('log/', DiaryEntryCreateView.as_view(), name='log-diary'),

    path('<int:pk>/', include([
        path('edit/', DiaryEntryEditView.as_view(), name='edit-diary'),
        path('delete/', DiaryEntryDeleteView.as_view(), name='delete-diary'),
        ]),
    ),

)
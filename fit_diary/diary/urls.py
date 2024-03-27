from django.urls import path

from fit_diary.diary.views import DiaryEntryCreateView, diary_view

urlpatterns = (
    path('', diary_view, name='diary'),
    path('log/', DiaryEntryCreateView.as_view(), name='log-diary'),
)